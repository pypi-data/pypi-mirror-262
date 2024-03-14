 # Unreal Engine Asset CLI
A linux-compatible command-line interface to download Assets from the Epic Game Store Marketplace. This is a re-implementation from [Allar's ue-mp-downloader](https://github.com/Allar/ue4-mp-downloader) or rather [its Fork](https://github.com/IncantaGames/ue-mp-downloader). A big shoutout to them, epsecially Allar, for figuring all this out!

## Features
- Download an Asset from the Marketplace
- List Assets from your EGS Library
- Get details about a specific Asset, like it's Version and what Engine Version is supported by each, or the description or author

## Legal
For this tool to work, you must have already accepted Epic's Terms (on account registration) and relevant EULAs (prompted when you open the Launcher for the first time or buy a marketplace item).
This tool can only download assets you own.

As with both original Repos: I, jwindgassen, mean no foul or infringement, and I will take this repo down immediately at the request of Epic Games if they do so.

## Usage
To use this tool, you can use the CLI it provides: `ue-assets`. To get help: `ue-assets --help`
The CLI provides a list of actions, that you can use:

 | Actions | Description |
 |---------|-------------|
 | login   | Login to the Epic Services. This will require an authentication code, which you must get by logging into your account [in your browser](https://www.epicgames.com/id/api/redirect?clientId=34a02cf8f4414e29b15921876da36f9a&responseType=code). The login will be stored in your keyring, so you don't need to enter in every time. |
 | list    | List the assets and their available Versions. |
 | details | Get the full details, including which Versions work with which Engine Version, for a specific detail. |
 | download | Download a given Asset + Version into a desired Directory on your system. |
 | logout | Logout from the Epic Services, i.e., removing the access token from the keyring. |

## Installation
The CLI can be installed from PyPI with `pip install ue-asset-cli`.
For developing, clone the repo and install the Package as editable with `pip intall -e .`.

## ToDo:
- More Login Method, primarily Username + Password.
- Interfacing with [ue4cli](https://github.com/adamrehn/ue4cli).
- More Caching, maybe usage of file instead of keyring??
- Better Output formatting
