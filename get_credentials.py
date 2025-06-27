import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def get_credentials(scopesUrl, pathCredentials: str, pathToken: str):

    creds = None

    if os.path.exists(pathToken):
        print("Path Token Exists")
        try:
            if os.path.getsize(pathToken) > 0:
                creds = Credentials.from_authorized_user_file(pathToken, scopesUrl)
            else:
                print(f"File '{pathToken}' is empty (0 bytes).")
        except FileNotFoundError:
            print("Path Token Not Found")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(pathCredentials, scopesUrl)
            creds = flow.run_local_server(port=0)

        with open(pathToken, 'w') as token:
            token.write(creds.to_json())

    return creds