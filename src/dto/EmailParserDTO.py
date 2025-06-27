
class EmailParserDTO:

    def __init__(self, payload, headers, body, date_time, file_path, file_name):
        self.payload = payload
        self.headers = headers
        self.body = body
        self.date_time = date_time
        self.file_path = file_path
        self.file_name = file_name
