import os
import re

from src.dto.FileDTO import FileDTO
from src.interfaces.IOSDirectoriesFiles import IOSDirectoriesFiles


class OSDirectoriesFiles(IOSDirectoriesFiles):

    def __init__(self):
        print("\n")

    def create_directory(self, directory_name) -> bool:
        try:
            os.makedirs(directory_name, exist_ok=True)
            print(f"Created directory '{directory_name}'  created successfully or already exists.")
            return True
        except OSError as e:
            print(f"Error creating directory '{directory_name}': {e}")
            return False

    def get_os_path_separator(self) -> str:
        return os.sep

    def get_path_app(self, path):
        str_tmp = path.split(";")
        return self.get_os_path_separator().join(str_tmp)

    def transform_env_prop_in_path(self, path) -> str:
        str_tmp = path.split(";")
        return self.get_os_path_separator().join(str_tmp)

    def create_file(self, file_dto: FileDTO) -> str:
        try:
            file_name = file_dto.file_name.replace(' ', '_').lower()
            file_name_array = file_name.split('.')
            print(file_name_array)
            file_name = re.sub(r'[^a-zA-Z0-9_]', '', file_name_array[0]) + "." + file_name_array[1]
            path = file_dto.file_path + self.get_os_path_separator() + file_name
            with open(path, "w", encoding="utf-8") as f:
                f.write(file_dto.mime_type)
                line = '-' * 100
                f.write(line)
                f.write(file_dto.content)
            print(f"File '{file_name}' created and written to successfully.")
            return file_name
        except IOError as e:
            print(f"Error creating file: {e}")
            return ""