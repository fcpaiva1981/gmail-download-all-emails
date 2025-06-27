import abc

from src.dto.FileDTO import FileDTO


class IOSDirectoriesFiles(abc.ABC):

    @abc.abstractmethod
    def create_directory(self, directory_name) -> bool:
        pass

    @abc.abstractmethod
    def get_os_path_separator(self) -> str:
        pass

    @abc.abstractmethod
    def get_path_app(self, path: str) -> str:
        pass

    @abc.abstractmethod
    def create_file(self, fileDto: FileDTO) -> str:
        pass