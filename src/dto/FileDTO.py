from dataclasses import dataclass


@dataclass
class FileDTO:

    def __init__(self, mime_type, content, file_path, file_name):
        self.mime_type = mime_type
        self.content = content
        self.file_path = file_path
        self.file_name = file_name





