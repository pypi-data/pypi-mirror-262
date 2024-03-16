from requests import Session
from pathlib import Path
import logging as log
from multiprocessing.pool import Pool
from tqdm import tqdm
from tempfile import mkdtemp
from zlib import decompress
import shutil
from .egs_types import AssetBuildInfo, AssetManifest, AssetChunk, dict_to_dataclass


# Pool function must be global, so we use this to store the Session to use for downloading
_SESSION: Session | None = None


def _download_chunk(values):
    """ Small helper for multiprocessing, does the main download and write-to-file task """
    chunk_data = _SESSION.get(values[0])
    chunk_data.raise_for_status()

    with open(values[1], "wb") as file:
        file.write(chunk_data.content)


def _hash_to_reverse_hex(hash: str) -> str:
    """
    ChunkHash to ReverseHexEncoding: Split Hash into chunks of 3, convert to 2-digit Hex, reverse and join
    Could be done with itertools.batched, but that's only 3.12
    """
    bytes = list(f"{int(hash[i*3:i*3+3]):02X}" for i in range(len(hash) // 3))
    return "".join(bytes[::-1])


class AssetDownloader:
    session: Session
    asset_id: str
    version_id: str
    output_dir: Path
    overwrite: bool
    cleanup: bool

    _download_dir: Path

    def __init__(
            self, session: Session, asset_id: str, version_id: str, *,
            output_dir: Path = None, overwrite: bool = True, cleanup: bool = True
    ):
        self.session = session
        self.asset_id = asset_id
        self.version_id = version_id
        self.output_dir = output_dir or Path("./asset_downloads")
        self.overwrite = overwrite
        self.cleanup = cleanup

        self.output_dir.mkdir(parents=True, exist_ok=self.overwrite)

    def download(self):
        log.info(f"Download directory: {self.output_dir.resolve()}")

        build_info = self._get_item_build_info()
        manifest = self._get_item_manifest(build_info)
        chunks = self._build_chunk_list(build_info, manifest)

        self._prepare_asset_download()
        chunk_dir = self._download_chunk_list(chunks)
        decompress_dir = self._decompress_asset_chunks(chunk_dir)
        extract_dir = self._extract_asset_chunks(manifest, decompress_dir)
        self._finalize_download(extract_dir)

        if self.cleanup:
            self._cleanup()

    @property
    def _build_info_url(self) -> str:
        return (f"https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/"
                f"assets/Windows/{self.asset_id}/{self.version_id}")

    def _get_item_build_info(self) -> AssetBuildInfo:
        log.info(f"Getting BuildInfo for {self.asset_id}")

        build_info = self.session.get(self._build_info_url, params={"label": "Live"})
        build_info.raise_for_status()

        build_info = dict_to_dataclass(AssetBuildInfo, build_info.json())
        log.debug(f"Build info: {build_info}")
        return build_info

    def _get_item_manifest(self, build_info: AssetBuildInfo) -> AssetManifest:
        log.info(f"Getting Manifest for {self.asset_id}")

        url_info = build_info.items.MANIFEST
        manifest = self.session.get(f"{url_info.distribution}{url_info.path}?{url_info.signature}")
        manifest.raise_for_status()

        manifest = dict_to_dataclass(AssetManifest, manifest.json())
        log.debug(f"Manifest: {manifest}")
        return manifest

    def _build_chunk_list(self, build_info: AssetBuildInfo, manifest: AssetManifest) -> list[AssetChunk]:
        log.info("Building ChunkList")

        chunk_path = build_info.items.CHUNKS.path
        chunk_base_url = build_info.items.CHUNKS.distribution + chunk_path[:chunk_path.rfind("/")] + "/ChunksV3/"

        chunks = []
        for chunk in manifest.ChunkHashList:
            hash = _hash_to_reverse_hex(manifest.ChunkHashList[chunk])
            group = f"{int(manifest.DataGroupList[chunk]):02d}"  # Leftpad
            filename = f"{chunk}.chunk"
            chunks.append(AssetChunk(chunk, hash, f"{chunk_base_url}{group}/{hash}_{chunk}.chunk", filename))

        log.debug(f"Chunks: {chunks}")
        return chunks

    def _prepare_asset_download(self):
        global _SESSION

        self._download_dir = Path(mkdtemp())
        log.debug(f"tempdir used for downloading: {self._download_dir}")

        _SESSION = self.session

    def _download_chunk_list(self, chunks: list[AssetChunk]) -> Path:
        chunk_dir = self._download_dir / "chunks"
        chunk_dir.mkdir()

        log.debug(f"Downloading Asset Chunks to {chunk_dir}")

        # Extract URL and Filename from chunk to use in Pool
        pool_inputs = ((chunk.url, str((chunk_dir / chunk.filename).resolve())) for chunk in chunks)

        with Pool() as pool:
            iterator = pool.imap_unordered(_download_chunk, pool_inputs, 5)
            list(tqdm(iterator, "Downloading Asset Chunks", total=len(chunks)))

        return chunk_dir

    def _decompress_asset_chunks(self, chunk_dir: Path) -> Path:
        decompress_dir = self._download_dir / "decompressed"
        decompress_dir.mkdir()

        log.debug(f"Decompressing Asset Chunks to {decompress_dir}")

        chunk_files = [chunk for chunk in chunk_dir.iterdir() if chunk.suffix == ".chunk"]
        for chunk_path in tqdm(chunk_files, "Decompressing Asset Chunks"):
            with open(chunk_path, "rb") as file_in, open(decompress_dir / chunk_path.name, "wb") as file_out:
                # We need the header (first 41 bytes) to get information about the chunk
                # TODO: Reference: Engine\Source\Runtime\Online\BuildPatchServices\Private\BuildPatchChunk.cpp (wrong)
                header = file_in.read(41)
                header_size = int(header[8])
                compressed = header[40] == 1

                # Junp to the end of the header and read the contents, decompressing them when needed
                file_in.seek(header_size)
                chunk_data = file_in.read()
                file_out.write(decompress(chunk_data) if compressed else chunk_data)

        return decompress_dir

    def _extract_asset_chunks(self, manifest: AssetManifest, decompress_dir: Path) -> Path:
        extract_dir = self._download_dir / "extracted"
        extract_dir.mkdir(parents=True, exist_ok=True)

        log.debug(f"Extracting Asset Chunks to {extract_dir.resolve()}")

        for file_list in tqdm(manifest.FileManifestList, "Extracting Chunks"):
            file_size = sum(int(_hash_to_reverse_hex(chunk_part.Size), 16) for chunk_part in file_list.FileChunkParts)

            # Read all chunks from the Manidest entry and combine them
            content = bytearray(file_size)
            offset = 0
            for chunk_part in file_list.FileChunkParts:
                chunk_guid = chunk_part.Guid
                chunk_offset = int(_hash_to_reverse_hex(chunk_part.Offset), 16)
                chunk_size = int(_hash_to_reverse_hex(chunk_part.Size), 16)

                chunk_dir = decompress_dir / f"{chunk_guid}.chunk"
                content[offset:offset + chunk_size] = chunk_dir.read_bytes()[chunk_offset:]

                offset += chunk_size

            # Write the combined content into the file
            file_path = extract_dir / file_list.Filename
            file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the parent folder exists
            file_path.write_bytes(content)

        return extract_dir

    def _finalize_download(self, extract_dir: Path):
        global _SESSION
        _SESSION = None

        log.info("Moving downloaded Asset to final location")
        log.debug(f"Moving extracted Assets from {extract_dir} to {self.output_dir.resolve()}")
        shutil.move(extract_dir, self.output_dir)

    def _cleanup(self):
        if self.cleanup:
            log.debug("Cleaning up the tempdir")
            shutil.rmtree(self._download_dir)
