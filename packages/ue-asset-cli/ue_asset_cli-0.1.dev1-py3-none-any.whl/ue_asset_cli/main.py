from pprint import pprint
from login import login, AuthenticationMethod
from library import get_assets
from downloader import AssetDownloader


if __name__ == '__main__':
    session, user_data = login(AuthenticationMethod.PROMPT)
    pprint(user_data)

    library = get_assets(session)

    asset = library[20]
    pprint(asset)
    print(asset.title)
    print(asset.versions)

    downloader = AssetDownloader(session, asset.catalogItemId, asset.builds["5.3"].appName)
    downloader.download()
