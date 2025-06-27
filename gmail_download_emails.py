import os.path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv


from get_credentials import get_credentials
from utils.read_email import get_email_body

from utils.format_datetime import format_date
from utils.read_email import get_email_headers

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
            headers = get_email_headers(payload['headers'])
            body = get_email_body(payload['body'])
            dateTime = format_date(headers[1])

            print(f"From: {headers[0]}")
            print(f"Date: {dateTime[1]}")
            print(f"Subject: {headers[2]}")
            print(f"Body:")
            print("-" * 30)
            print(f"\n{body}")



    except HttpError as error:
        print(f"An HTTP error occurred: {error}")


if __name__ == '__main__':
    main()





