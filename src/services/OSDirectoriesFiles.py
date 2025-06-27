import os
import re

from src.dto.FileDTO import FileDTO
from src.interfaces.IOSDirectoriesFiles import IOSDirectoriesFiles

class OSDirectoriesFiles(IOSDirectoriesFiles):

    def createDirectory(self, directory_name) -> bool:
        try:
            os.makedirs(directory_name, exist_ok=True)
            print(f"Created directory '{directory_name}'  created successfully or already exists.")
            return True
        except OSError as e:
            print(f"Error creating directory '{directory_name}': {e}")
            return False

    def getOsPathSeparator(self) -> str:
        return os.sep

    def getPathApp(self, path) -> str:
        str_tmp = path.split(";")
        return self.getOsPathSeparator().join(str_tmp)

    def createFile(self, fileDto:FileDTO) -> str:
        try:
            file_name = fileDto.replace(' ', '_').lower()
            file_name_array = file_name.split('.')
            file_name = re.sub(r'[^a-zA-Z0-9_]', '', file_name_array[0]) + "_" + file_name_array[1] + "." + \
                        file_name_array[2]
            path = fileDto.file_path + self.getOsPathSeparator()  + file_name
            with open(path, "w", encoding="utf-8") as f:
                f.write(fileDto.content)
            print(f"File '{file_name}' created and written to successfully.")
            return file_name
        except IOError as e:
            print(f"Error creating file: {e}")
            return ""