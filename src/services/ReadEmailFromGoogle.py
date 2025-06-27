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

    def __init__(self, creds, envs: EnvsDTO):
        self.envs = envs
        self.credentials = creds

    def get_email_body(self, payload):
        plain_text_content = ""
        html_content = ""
        other_content = ""
        mime_type = ""
        errors = []

        if not payload:
            errors.append("The initial payload was empty or None.")
            return EmailBodyDTO(plain_text_content, html_content, errors)

        parts_to_process = [payload]

        while parts_to_process:
            plain_text_content = ""
            html_content = ""
            mime_type = ""
            other_content = ""
            errors = []
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
                    if not plain_text_content:
                        plain_text_content = "NO CONTENT"
                elif 'text/html' in mime_type:
                    html_content += decoded_data
                    if not html_content:
                        html_content = "NO CONTENT"
                else:
                    other_content += decoded_data
                    if not other_content:
                        other_content = "NO CONTENT OTHER"

            except (binascii.Error, UnicodeDecodeError) as e:
                errors.append(e)
                continue

        return EmailBodyDTO(mime_type, plain_text_content, html_content, other_content, errors)

    def get_email_headers(self, payload) -> HeadersDTO:
        headers = payload.get('headers')
        subject = next((d['value'] for d in headers if d['name'] == 'Subject'), None)
        sender = next((d['value'] for d in headers if d['name'] == 'From'), None)
        date_header = next((d['value'] for d in headers if d['name'] == 'Date'), None)
        return HeadersDTO(sender, date_header, subject)

    def pars_email(self, payload, id_message) -> EmailParserDTO:
        try:
            content = ""
            osUtils = OSDirectoriesFiles()
            utils = UtilsFunctions()
            headers = self.get_email_headers(payload)
            body = self.get_email_body(payload)
            date = utils.format_date(headers.date_header)
            email_data = EmailDataDTO(id_message,
                                      headers,
                                      body,
                                      date)

            directory_path = self.envs.path_output_data + osUtils.get_os_path_separator() + email_data.date_time.date_without_time

            osUtils.create_directory(directory_path)

            file = email_data.headers.sender.split('<')[0]
            file = file.replace('.', '_')
            file = file.strip() + "_" + email_data.date_time.date_to_create_directory

            if len(email_data.body.txt.strip()) > 0:
                print(f"Tamanhho: {len(email_data.body.txt.strip())}")
                file = file + ".txt"
                content = email_data.body.txt

            if len(email_data.body.html.strip()) > 0:
                print(f"Tamanhho: {len(email_data.body.html.strip())}")
                file = file + ".html"
                content = email_data.body.html

            if len(email_data.body.others.strip()) > 0:
                print(f"Tamanhho: {len(email_data.body.others.strip())}")
                file = file + ".otr"
                content = email_data.body.others

            if len(email_data.body.errors) > 0:
                print(f"Tamanhho: {len(email_data.body.errors)}")
                file = file + ".log"
                content = '\n'.join(email_data.body.errors)

            if not content:
                file = file + ".txt"

            if not email_data.body.mime_type:
                email_data.body.mime_type = "other"

            osUtils.create_file(FileDTO(email_data.body.mime_type, content, directory_path, file))

            email_parsed =  EmailParserDTO(payload, email_data.headers, email_data.body, email_data.date_time, directory_path,
                                              file)
            self.show_email_data(email_data)
            return email_parsed

        except HttpError as error:
            print(f"An HTTP error occurred: {error}")

    def show_email_data(self, email_data: EmailDataDTO):
        print(f"Msg ID: {email_data.message_id}")
        print(f"MimeType: {email_data.body.mime_type}")
        print(f"From: {email_data.headers.sender}")
        print(f"Date: {email_data.date_time.formated_date_full}")
        print(f"Subject: {email_data.headers.subject}")
        print("-" * 100)
