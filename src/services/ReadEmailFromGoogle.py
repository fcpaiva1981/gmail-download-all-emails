import base64
import binascii
from googleapiclient.errors import HttpError
from src.dto.EmailBodyDTO import EmailBodyDTO
from src.dto.EmailDataDTO import EmailDataDTO
from src.dto.EmailParserDTO import EmailParserDTO
from src.dto.EnvsDTO import EnvsDTO
from src.dto.FileDTO import FileDTO
from src.dto.HeadersDTO import HeadersDTO
from src.interfaces.IReadEmailFromGoogle import IReadEmailFromGoogle
from src.services.OSDirectoriesFiles import OSDirectoriesFiles
from src.services.UtilsFunctions import UtilsFunctions


class ReadEmailFromGoogle(IReadEmailFromGoogle):

    def __init__(self, envs: EnvsDTO):
        self.envs = envs

    def getEmailBody(self, payload):
        plain_text_content = ""
        html_content = ""
        errors = []

        if not payload:
            errors.append("The initial payload was empty or None.")
            return EmailBodyDTO(plain_text_content, html_content, errors)

        parts_to_process = [payload]

        while parts_to_process:
            part = parts_to_process.pop(0)

            if 'parts' in part and part.get('parts'):
                parts_to_process.extend(part['parts'])
                continue

            body = part.get('body')
            if not body:
                continue

            data = body.get('data')
            if not data:
                continue

            mime_type = part.get('mimeType', '')

            try:
                decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')

                if 'text/plain' in mime_type:
                    plain_text_content += decoded_data
                elif 'text/html' in mime_type:
                    html_content += decoded_data

            except (binascii.Error, UnicodeDecodeError) as e:
                errors.append(e)
                continue

        return EmailBodyDTO(plain_text_content, html_content, errors)

    def getEmailHeaders(self, payload) -> HeadersDTO:
        headers = payload.get('headers')
        subject = next((d['value'] for d in headers if d['name'] == 'Subject'), None)
        sender = next((d['value'] for d in headers if d['name'] == 'From'), None)
        date_header = next((d['value'] for d in headers if d['name'] == 'Date'), None)
        return HeadersDTO(sender=sender, date_header=date_header, subject=subject)

    def parseEmail(self, payload, id_message) -> EmailParserDTO:
        try:
            email_data = EmailDataDTO()
            osUtils = OSDirectoriesFiles()
            utils = UtilsFunctions()

            email_data.headers = self.getEmailHeaders(payload)
            email_data.body = self.getEmailBody(payload)
            email_data.date_time = utils.formatDate(email_data.headers.date_header[1])

            directory_path = (self.envs.path_output_data()
                              + osUtils.getOsPathSeparator()
                              + email_data.date_time[2])

            osUtils.createDirectory(directory_path)

            file = email_data.headers.sender.split('<')[0]
            file = file.strip()+"."+email_data.date_time[3]

            if len(email_data.body.txt.strip()) > 0:
                print(f"\n{len(email_data.body.txt.strip())}")
                file = file + ".txt"
                content = email_data.body.txt

            if len(email_data.body.html.strip()) > 0:
                print(f"\n{len(email_data.body.html.strip())}")
                file = file + ".html"
                content = email_data.body.html

            if len(email_data.body.errors) > 0:
                print(f"\n{len(email_data.body.errors)}")
                file = file + ".log"
                content = '\n'.join(email_data.body.errors)


            osUtils.createFile( FileDTO(content, directory_path , file))

        except HttpError as error:
            print(f"An HTTP error occurred: {error}")


    def showEmailData(self, email_data: EmailDataDTO):
        print(f"Msg ID: {email_data.message_id}")
        print(f"From: {email_data.headers.sender}")
        print(f"Date: {email_data.date_time[1]}")
        print(f"Subject: {email_data.headers.subject}")
        print(f"Body:")
        print("-" * 100)
