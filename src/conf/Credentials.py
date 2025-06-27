import os.path
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from src.dto.EnvsDTO import EnvsDTO
from src.services.OSDirectoriesFiles import OSDirectoriesFiles
from src.interfaces.ICredentialsGmail import ICredentialsGmail


class CredentialsGmail(ICredentialsGmail):

    def __init__(self):
        load_dotenv()
        self.osDirectoriesFiles = OSDirectoriesFiles()
        self.envsDTO = None

    def getCredentials(self):
        creds = None

        if os.path.exists(self.envsDTO.path_token):
            print("Path Token Exists")
            try:
                if os.path.getsize(self.envsDTO.path_token) > 0:
                    creds = Credentials.from_authorized_user_file(self.envsDTO.path_token, self.envsDTO.scopesUrl)
                else:
                    print(f"File '{self.envsDTO.path_token}' is empty (0 bytes).")
            except FileNotFoundError:
                print("Path Token Not Found")

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.envsDTO.path_credentials, self.envsDTO.scopesUrl)
                creds = flow.run_local_server(port=0)

            with open(self.envsDTO.path_token, 'w') as token:
                token.write(creds.to_json())

        return creds

    def getEnvs(self):
        load_dotenv()

        self.envsDTO = EnvsDTO(os.getenv('SCOPES'),os.getenv('PATH_CREDNTIALS'), os.getenv('PATH_TOKEN'), )

        print("=" * 100)
        print(f"SCOPES: {self.envsDTO.scopesUrl}")
        print(f"Credentials: {self.envsDTO.path_credentials}")
        print(f"Path Token: {self.envsDTO.path_token}")
        print(f"Path Output Data: {self.envsDTO.path_output_data}")
        print("=" * 100)