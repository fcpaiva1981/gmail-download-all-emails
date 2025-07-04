import os.path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv


from get_credentials import get_credentials
from utils.create_directory import get_path_os, create_directory, get_path_os_separator
from utils.create_file_from_email import create_file
from utils.read_email import get_email_body

from utils.format_datetime import format_date
from utils.read_email import get_email_headers

load_dotenv()

scopesUrl = os.getenv('SCOPES')
path_credentials = os.getenv('PATH_CREDNTIALS')
path_token = os.getenv('PATH_TOKEN')
path_output_data = os.getenv('OUTPUT_DATA')

path_credentials = get_path_os(path_credentials)
path_token = get_path_os(path_token)
path_output_data = get_path_os(path_output_data)

SCOPES = [scopesUrl]

print("=" * 100)
print(f"SCOPES: {SCOPES}")
print(f"Credentials: {path_credentials}")
print(f"Path Token: {path_token}")
print(f"Path Output Data: {path_output_data}")
print("=" * 100)

def main():
    creds = get_credentials(SCOPES, path_credentials, path_token)

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
            headers = get_email_headers(payload.get('headers'))
            body = get_email_body(payload)
            date_time = format_date(headers[1])

            file_path = path_output_data+get_path_os_separator()+date_time[2]
            create_directory(file_path)

            print(f"Msg ID: {message['id']}")
            print(f"From: {headers[0]}")
            print(f"Date: {date_time[1]}")
            print(f"Subject: {headers[2]}")
            print(f"Body:")
            print("-" * 100)

            file_from_name = headers[0].split('<')[0]
            file_from_name = file_from_name.strip()+"."+date_time[3]

            if len(body.get('text').strip()) > 0:
                print(f"\n{len(body.get('text').strip())}")
                file_from_name = file_from_name + ".txt"
                content = body.get('text')

            if len(body.get('html').strip()) > 0:
                print(f"\n{len(body.get('html').strip())}")
                file_from_name = file_from_name + ".html"
                content = body.get('html')

            if len(body.get('errors')) > 0:
                print(f"\n{len(body.get('errors'))}")
                file_from_name = file_from_name + ".log"
                content = '\n'.join(len(body.get('errors')))

            create_file(content, file_path, file_from_name)

    except HttpError as error:
        print(f"An HTTP error occurred: {error}")


if __name__ == '__main__':
    main()





