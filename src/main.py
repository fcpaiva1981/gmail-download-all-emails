import time
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.conf.Credentials import CredentialsGmail
from src.services.ReadEmailFromGoogle import ReadEmailFromGoogle
from src.services.UtilsFunctions import UtilsFunctions


def main():
     hora_inicio = datetime.now()
     print(f"Hora de início: {hora_inicio.strftime('%H:%M:%S')}")
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

          total_message = len(messages)
          print(f"Found {total_message} messages.")
          i = 1
          for message in messages:
               msg = service.users().messages().get(userId='me', id=message['id']).execute()
               payload = msg.get('payload')
               read_email_from_google.pars_email(payload, message['id'],total_message, i )
               i = i + 1

          hora_fim = datetime.now()
          print(f"Hora de fim: {hora_fim.strftime('%H:%M:%S')}")

          duracao = hora_fim - hora_inicio
          print(f"\nDuração total: {duracao}")
     except HttpError as error:
          print(f"An HTTP error occurred: {error}")


if __name__ == '__main__':
    main()
