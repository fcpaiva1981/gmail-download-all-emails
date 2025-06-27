import base64

def get_email_body(payload):
    if 'parts' in payload:
        for part in payload['parts']:
            body = get_email_body(part)
            if body:
                return body
    elif payload.get('mimeType') == 'text/plain':
        data = payload.get('body', {}).get('data')
        if data:
            return base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')
    elif 'body' in payload and 'data' in payload['body']:
        data = payload['body']['data']
        return base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')
    return ""

def get_email_headers(headers):
    subject = next((d['value'] for d in headers if d['name'] == 'Subject'), None)
    sender = next((d['value'] for d in headers if d['name'] == 'From'), None)
    date_header = next((d['value'] for d in headers if d['name'] == 'Date'), None)
    return [sender, date_header, subject]
