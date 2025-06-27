from dataclasses import dataclass


@dataclass
class FileDTO:

    def __init__(self, content, file_path, file_name):
        self.content = content
        self.file_path = file_path
        self.file_name = file_name





