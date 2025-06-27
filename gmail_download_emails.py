import os.path
import base64
import locale
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from datetime import datetime

from get_credentials import get_credentials

#Load .env
load_dotenv()

scopesUrl = os.getenv('SCOPES')
pathCredentials = os.getenv('PATH_CREDNTIALS')
pathToken = os.getenv('PATH_TOKEN')

SCOPES = [scopesUrl]

print("==================================")
print(f"SCOPES: {SCOPES}")
print(f"Credentials: {pathCredentials}")
print(f"Path Token: {pathToken}")
print("==================================")

def main():
    creds = get_credentials(SCOPES, pathCredentials, pathToken)


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
            payload = msg['payload']
            headers = payload['headers']
            subject = next((d['value'] for d in headers if d['name'] == 'Subject'), None)
            sender = next((d['value'] for d in headers if d['name'] == 'From'), None)
            date_header = next((d['value'] for d in headers if d['name'] == 'Date'), None)
            if date_header != emailDate:
                emailDate = date_header


            print(f"From: {sender}")
            print(f"Date: {emailDate}")
            print(f"Subject: {subject}")

            if 'parts' in payload:
                parts = payload['parts']
                if len(parts[0]['body']) > 0:
                    if len(parts[0]['body']['data']) > 0:
                        data = parts[0]['body']['data']
                    else:
                        data = "No body"
                else:
                    data = "No body"
            else:
                if len(parts[0]['body']['data']) > 0:
                    data = payload['body']['data']
                else:
                    data = "No body"

            data = data.replace("-","+").replace("_","/")

            if len(data.strip()) > 0 and  data not in "No body":
                decoded_data = base64.b64decode(data)
                print(f"Body snippet: {decoded_data}...")
                print("-" * 30)

    except HttpError as error:
        print(f"An HTTP error occurred: {error}")

def formatDate():
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        print("Locale 'pt_BR.UTF-8' não encontrado. Tentando 'Portuguese_Brazil'.")
        try:
            locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil')
        except locale.Error:
            print("Locale para Português do Brasil não encontrado no sistema.")

    agora = datetime.now()

    formato_pt_br = agora.strftime("%A, %d de %B de %Y")
    
    print(formato_pt_br)

    datas = [agora, formato_pt_br]

    return

if __name__ == '__main__':
    main()





