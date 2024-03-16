import argparse
from importlib.metadata import metadata
from pathlib import Path
import logging as log

from .login import login, logout, AuthenticationMethod
from .library import get_assets
from .downloader import AssetDownloader


_metadata = metadata("ue_asset_cli")


def make_parser():
    parser = argparse.ArgumentParser(prog=_metadata["name"], description=_metadata["description"])
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("-d", "--debug", action="store_true")

    subparsers = parser.add_subparsers(title="Subcommands", dest="command", required=True)

    # Login
    login_parser = subparsers.add_parser("login", description="Login to the Epic Game Store")
    login_parser.add_argument("method", choices=["promt", "browser"])

    # Logout
    subparsers.add_parser("logout", description="Logout from the Epic Game Store")

    # ToDo: User
    # user_parser = subparsers.add_parser("user", description="Show user information")
    # user_parser.add_argument("--full", action="store_true")

    # List
    subparsers.add_parser("list", description="List the assets in the Library")

    # Details
    detail_parser = subparsers.add_parser("details", description="Details about a specific asset")
    detail_parser.add_argument("title", help="Title of the asset")

    # Download
    download_parser = subparsers.add_parser("download", description="Downloads an asset from the Epic Game Store")
    download_parser.add_argument("title", help="Title of the asset")
    download_parser.add_argument("asset_version", help="Which Version to download")
    download_parser.add_argument("path", default="./asset_downloads", help="Path to put the asset in")
    download_parser.add_argument(
        "-f", "--force", "--overwrite", dest="overwrite", action="store_true",
        help="Overwrite the existing download directory if it exists. Errors when directory exists otherwise"
    )
    download_parser.add_argument("--no-cleanup", default=False, help="Do not clear the artifact tempdir")

    return parser


def _login(args):
    login(AuthenticationMethod.PROMPT if args.method == "prompt" else AuthenticationMethod.BROWSER)


def _logout(args):
    logout()


def _list(args):
    session, user_data = login()
    assets = get_assets(session)

    print("Assets:")
    for asset in assets:
        print(f"  {asset.title} -> {asset.versions}")


def _details(args):
    session, user_data = login()
    assets = get_assets(session)

    selected_asset = next((asset for asset in assets if asset.title == args.title), None)
    if selected_asset is None:
        raise ValueError(f"Could not find asset with title {args.title!r}")

    print(selected_asset)

def _download(args):
    session, user_data = login()
    assets = get_assets(session)

    selected_asset = next((asset for asset in assets if asset.title == args.title), None)
    build = selected_asset.builds[args.asset_version]

    downloader = AssetDownloader(
        session, selected_asset.catalogItemId, build.appName,
        output_dir=Path(args.path), overwrite=args.overwrite, cleanup=not args.no_cleanup
    )
    downloader.download()


SUBCOMMANDS = {
    "login": _login,
    "logout": _logout,
    "list": _list,
    "details": _details,
    "download": _download
}

def main():
    args = make_parser().parse_args()

    log.basicConfig(level=log.DEBUG if args.debug else log.INFO)

    if args.version:
        print(f"{_metadata['name']} Version: {_metadata['version']}")
        return

    # Call subcommand
    SUBCOMMANDS[args.command](args)
