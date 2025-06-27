from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.conf.Credentials import CredentialsGmail
from src.services.ReadEmailFromGoogle import ReadEmailFromGoogle
from src.services.UtilsFunctions import UtilsFunctions


def main():
     gmail_credentials = CredentialsGmail()
     envs = gmail_credentials.get_envs()
     read_email_from_google = ReadEmailFromGoogle(gmail_credentials.getCredentials(), envs)
     creds = gmail_credentials.getCredentials()
     utils = UtilsFunctions()

     try:
          service = build('gmail', 'v1', credentials=creds)
          results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
          messages = results.get('messages', [])

          if not messages:
               print("No messages found.")
               return

          print(f"Found {len(messages)} messages.")

          for message in messages:
               msg = service.users().messages().get(userId='me', id=message['id']).execute()
               payload = msg.get('payload')
               read_email_from_google.pars_email(payload, message['id'])

     except HttpError as error:
          print(f"An HTTP error occurred: {error}")


if __name__ == '__main__':
    main()
