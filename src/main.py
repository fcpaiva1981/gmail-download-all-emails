from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.conf.Credentials import CredentialsGmail
from src.services.ReadEmailFromGoogle import ReadEmailFromGoogle




def main():
     gmail_credentials = CredentialsGmail()
     read_email_from_google = ReadEmailFromGoogle()
     creds = gmail_credentials.getCredentials()

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
               emailParsed=  read_email_from_google.parseEmail(msg.get('payload'))

               create_directory(file_path)

               print(f"Msg ID: {message['id']}")
               print(f"From: {headers[0]}")
               print(f"Date: {date_time[1]}")
               print(f"Subject: {headers[2]}")
               print(f"Body:")
               print("-" * 100)

               file_from_name = headers[0].split('<')[0]
               file_from_name = file_from_name.strip() + "." + date_time[3]

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
