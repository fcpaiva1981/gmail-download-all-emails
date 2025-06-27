import os.path

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from src.dto.EnvsDTO import EnvsDTO
from src.interfaces.ICredentialsGmail import ICredentialsGmail
from src.services.OSDirectoriesFiles import OSDirectoriesFiles


class CredentialsGmail(ICredentialsGmail):


    def getCredentials(self):
        envs_DTO = self.get_envs()
        creds = None

        if os.path.exists(envs_DTO.path_token):
            print("Path Token Exists")
            try:
                if os.path.getsize(envs_DTO.path_token) > 0:
                    creds = Credentials.from_authorized_user_file(envs_DTO.path_token, envs_DTO.scopesUrl)
                else:
                    print(f"File '{envs_DTO.path_token}' is empty (0 bytes).")
            except FileNotFoundError:
                print("Path Token Not Found")

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(envs_DTO.path_credentials, envs_DTO.scopesUrl)
                creds = flow.run_local_server(port=0)

            with open(envs_DTO.path_token, 'w') as token:
                token.write(creds.to_json())

        return creds

    def get_envs(self) -> EnvsDTO:
        load_dotenv()

        events_data = EnvsDTO(os.getenv('SCOPES'),
                              os.getenv('PATH_CREDNTIALS'),
                              os.getenv('PATH_TOKEN'),
                              os.getenv('OUTPUT_DATA'))

        envs_DTO = self.fix_paths(events_data)

        print("=" * 100)
        print(f"SCOPES: {envs_DTO.scopesUrl}")
        print(f"Credentials: {envs_DTO.path_credentials}")
        print(f"Path Token: {envs_DTO.path_token}")
        print(f"Path Output Data: {envs_DTO.path_output_data}")
        print("=" * 100)

        return envs_DTO

    def fix_paths(self, events_data) -> EnvsDTO:
        osUtils = OSDirectoriesFiles()
        events_data.path_credentials = osUtils.get_path_app(events_data.path_credentials)
        events_data.path_token = osUtils.get_path_app(events_data.path_token)
        events_data.path_output_data = osUtils.get_path_app(events_data.path_output_data)
        return events_data
