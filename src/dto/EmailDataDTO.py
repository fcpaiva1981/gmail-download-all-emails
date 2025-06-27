

class EmailDataDTO():

    def __init__(self, message_id,  headers, body, date_time):
        self.message_id = message_id
        self.headers = headers
        self.body = body
        self.date_time = date_time
