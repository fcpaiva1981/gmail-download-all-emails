import base64
import binascii


def get_email_body(payload):
    plain_text_content = ""
    html_content = ""
    errors = []

    if not payload:
        errors.append("The initial payload was empty or None.")
        return {'text':plain_text_content, 'html':html_content, 'errors':errors}

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

        decoded_data = None

        try:
            decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
        except (binascii.Error, UnicodeDecodeError) as e:
            errors.append(e)
            continue

        mime_type = part.get('mimeType', '')
        if 'text/plain' in mime_type:
            plain_text_content += decoded_data
        elif 'text/html' in mime_type:
            html_content += decoded_data

        return {'text': plain_text_content, 'html': html_content, 'errors': errors}

def get_email_headers(headers):
    subject = next((d['value'] for d in headers if d['name'] == 'Subject'), None)
    sender = next((d['value'] for d in headers if d['name'] == 'From'), None)
    date_header = next((d['value'] for d in headers if d['name'] == 'Date'), None)
    return [sender, date_header, subject]
