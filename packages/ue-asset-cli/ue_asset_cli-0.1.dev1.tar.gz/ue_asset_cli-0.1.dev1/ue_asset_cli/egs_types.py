from dataclasses import dataclass, fields, is_dataclass
from typing import Any, get_args, TypeVar


T = TypeVar("T")


def dict_to_dataclass(cls: type[T], value) -> T:
    if is_dataclass(cls):
        fieldtypes = {f.name: f.type for f in fields(cls)}
        return cls(**{f: dict_to_dataclass(fieldtypes[f], value[f]) for f in fieldtypes})
    elif isinstance(value, list):
        return [dict_to_dataclass(get_args(cls)[0], item) for item in value]

    return value


@dataclass
class UserData:
    # ToDo: display_name: str
    account_id: str
    token: str
    token_type: str
    auth_time : str
    expires_at: str
    expires_in: int
    # ToDo: Refresh Tokens?


@dataclass
class AssetItem:
    @dataclass
    class Build:
        appName: str  # ToDo: These 2 seem to be the same?!
        # appId: str
        assetId: str
        id: str
        buildVersion: str
        versionTitle: str | None
        compatibleApps: list[str]
        platforms: list[str]

    title: str
    catalogItemId: str
    labelName: str
    namespace: str
    id: str
    builds: dict[str, Build]
    categories: list[str]
    developer: str
    description: str

    @property
    def versions(self):
        return list(self.builds.keys())


@dataclass
class AssetBuildInfo:
    @dataclass
    class Item:
        @dataclass
        class Manifest:
            signature: str
            distribution: str
            path: str
            hash: str
            additionalDistributions: list[str]

        @dataclass
        class Chunks:
            signature: str
            distribution: str
            path: str
            additionalDistributions: list[str]

        MANIFEST: Manifest
        CHUNKS: Chunks

    appName: str
    labelName: str
    buildVersion: str
    catalogItemId: str
    metadata: Any
    expires: str
    items: Item
    assetId: str

@dataclass
class AssetManifest:
    @dataclass
    class FileManifest:
        @dataclass
        class ChunkPart:
            Guid: str
            Offset: str
            Size: str

        Filename: str
        FileHash: str
        FileChunkParts: list[ChunkPart]

    ManifestFileVersion: str
    bIsFileData: bool
    AppID: str
    AppNameString: str
    BuildVersionString: str
    LaunchExeString: str
    LaunchCommand: str
    PrereqIds: list[str]
    PrereqName: str
    PrereqPath: str
    PrereqArgs: str
    FileManifestList: list[FileManifest]
    ChunkHashList: dict[str, str]
    ChunkShaList: dict[str, str]
    DataGroupList: dict[str, str]
    ChunkFilesizeList: dict[str, str]
    CustomFields: dict

@dataclass
class AssetChunk:
    guid: str
    hash: str
    url: str
    filename: str
