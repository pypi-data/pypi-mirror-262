from requests.sessions import Session, HTTPAdapter
from enum import Enum, auto
import keyring
import logging as log
import sys, os, subprocess
from .egs_types import UserData, dict_to_dataclass


KEYRING_NAME = "ue_asset_cli"

CLIENT_ID = "34a02cf8f4414e29b15921876da36f9a"
CLIENT_SECRET = "daafbccc737745039dffe53d94fc76cf"

REDIRECT_URL = f"https://www.epicgames.com/id/api/redirect?clientId={CLIENT_ID}&responseType=code"
TOKEN_URL = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
VERIFY_URL = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/verify"


class AuthenticationMethod(Enum):
    PROMPT = auto()
    BROWSER = auto()


def _get_authentication_code(method: AuthenticationMethod) -> str:
    if method == AuthenticationMethod.BROWSER:
        log.info("Login in the Browser and input the 'authenticationCode'")

        if sys.platform == "win32":
            os.startfile(REDIRECT_URL)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", REDIRECT_URL])
        else:
            try:
                subprocess.Popen(["xdg-open", REDIRECT_URL])
            except OSError:
                log.info(f"Please open a browser on: {REDIRECT_URL}")

        return input("Authentication Code: ")
    if method == AuthenticationMethod.PROMPT:
        return input("Autehntication Code: ")

def _login_with_authentication_code(session: Session, authentication_code: str) -> dict | None:
    data = {
        "grant_type": "authorization_code",
        "code": authentication_code,
        "token": "eg1"
    }

    user_data = session.post(TOKEN_URL, data, auth=(CLIENT_ID, CLIENT_SECRET))
    user_data.raise_for_status()

    if user_data.status_code == 200:
        log.info("Successful login with authentication code")
        return user_data.json()
    else:
        log.error("Could not login with Authentication Code")
        return None

def _verify_authentication_token(session: Session, token: str) -> dict | None:
    session.headers["Authorization"] = f"bearer {token}"
    user_data = session.get(VERIFY_URL)

    if user_data.status_code == 200:
        log.info("Authentication Token successfully verified")
        return user_data.json()
    else:
        log.error("Could not verify Authentication Token")
        return None

def login(authentication_method: AuthenticationMethod = AuthenticationMethod.BROWSER) -> tuple[Session, UserData]:
    session = Session()
    session.mount("https://", HTTPAdapter(max_retries=10))  # More retries, for good measure

    auth_code = keyring.get_password(KEYRING_NAME, "access_token")
    if auth_code is None:
        auth_code = _get_authentication_code(authentication_method)
        user_data = _login_with_authentication_code(session, auth_code)
        user_data["token"] = user_data["access_token"]  # ToDo: Login and Verify yield different fields
    else:
        user_data = _verify_authentication_token(session, auth_code)

    # Try again
    if user_data is None:
        keyring.delete_password(KEYRING_NAME, "access_token")
        return login(authentication_method)

    user_data = dict_to_dataclass(UserData, user_data)

    access_token = user_data.token
    session.headers["Authorization"] = f"bearer {access_token}"
    keyring.set_password(KEYRING_NAME, "access_token", access_token)

    return session, user_data


def logout(session: Session | None = None):
    log.info("Logging out")
    keyring.delete_password(KEYRING_NAME, "access_token")
    if session is not None:
        session.close()
