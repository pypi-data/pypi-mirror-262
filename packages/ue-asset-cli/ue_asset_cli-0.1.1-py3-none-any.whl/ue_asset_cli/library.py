from requests import Session
from tqdm import tqdm
from collections import defaultdict
from re import match
from .egs_types import AssetItem


ASSETS_URL = "https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/Windows?label=Live"
DETAILS_URL = "https://catalog-public-service-prod06.ol.epicgames.com/catalog/api/shared/bulk/items"


def _asset_list(session: Session) -> list[dict]:
    assets = session.get(ASSETS_URL)
    assets.raise_for_status()
    assets = [asset for asset in assets.json() if asset["namespace"].lower() == "ue"]

    return assets


def _get_asset_details(session: Session, catalog_id: str) -> dict | None:
    details = session.get(DETAILS_URL, params={
        "id": catalog_id,
        "includeDLCDetails": False,
        "includeMainGameDetails": False,
        "country": "US",
        "locale": "en"
    })
    details.raise_for_status()
    return details.json()[catalog_id]


def _merge_asset_details(assets: list[dict], details: dict) -> AssetItem:
    assets_by_name = {asset["appName"]: asset for asset in assets}

    builds = []
    for release_info in details["releaseInfo"]:
        asset = assets_by_name[release_info["appId"]]  # Join by appName / appId
        builds.append(AssetItem.Build(
            appName = asset["appName"],
            assetId = asset["assetId"],
            id = release_info["id"],
            buildVersion = asset["buildVersion"],
            versionTitle = release_info.get("versionTitle", None),
            compatibleApps = release_info["compatibleApps"],
            platforms = release_info["platform"],
        ))

    builds = {match(r"(\d+\.\d+)", build.buildVersion).group(0): build for build in builds}

    return AssetItem(
        title = details["title"],
        catalogItemId = assets[0]["catalogItemId"],
        labelName = assets[0]["labelName"],
        namespace = details["namespace"],
        id = details["id"],
        builds = builds,
        categories = [catagory["path"] for catagory in details["categories"]],
        developer = details["developer"],
        description = details["description"],
    )

def get_assets(session: Session) -> list[AssetItem]:
    assets = _asset_list(session)
    assets = [asset for asset in assets if asset["assetId"] != "UE"]  # Filter out engines

    # Asset details are identical for all build Versions, only depending on the catalogItmId
    # We group all assets by their catalogItmId into a multimap and merge the versions afterwards
    grouped_assets = defaultdict(list)
    for asset in assets:
        grouped_assets[asset["catalogItemId"]].append(asset)

    # Get details for each asset
    assets = []
    for item_id in tqdm(grouped_assets.keys(), desc="Downloading Asset Details"):
        details = _get_asset_details(session, item_id)

        # Only allow download of assets, projects and plugins
        # Engine types should have been filtered out above, so I don't know, if this is really neccessary
        if not any(category["path"] in ("assets", "projects", "plugins") for category in details["categories"]):
            continue

        merged = _merge_asset_details(grouped_assets[item_id], details)
        assets.append(merged)

    # Sort by title
    assets.sort(key=lambda asset: asset.title)
    return assets