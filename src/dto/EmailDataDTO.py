

class EmailDataDTO():

    def __init__(self, message_id,  headers, body, date_time, path, path_created , file_name, index, total):
        self.message_id = message_id
        self.headers = headers
        self.body = body
        self.date_time = date_time
        self.path = path
        self.path_created = path_created
        self.file_name = file_name
        self.index = index
        self.total = total
