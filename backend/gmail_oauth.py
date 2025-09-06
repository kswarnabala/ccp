# gmail_oauth.py
import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

CLIENT_SECRETS_FILE = "client_secret.json"  # place your OAuth client JSON here
TOKEN_FILE = "token.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def authenticate_gmail(start_browser: bool = True) -> str:
    """
    Launches the installed app flow and saves token.json.
    If start_browser=True, opens a local browser to sign in (run_local_server).
    Returns the auth URL (or message) for debugging.
    """
    if not os.path.exists(CLIENT_SECRETS_FILE):
        raise FileNotFoundError(f"{CLIENT_SECRETS_FILE} not found. Put your Google client JSON here.")

    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES
    )

    if start_browser:
        # This will open a local port and perform callback automatically, then return credentials.
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        return "Authenticated and token saved."
    else:
        auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
        return auth_url

def load_gmail_token():
    """
    Load stored credentials (if present) as google.oauth2.credentials.Credentials.
    """
    if not os.path.exists(TOKEN_FILE):
        return None
    try:
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        return creds
    except Exception:
        return None
