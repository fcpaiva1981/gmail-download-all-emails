import abc

from src.dto.FileDTO import FileDTO


class IOSDirectoriesFiles(abc.ABC):

    @abc.abstractmethod
    def createDirectory(self, directory_name) -> bool:
        pass

    @abc.abstractmethod
    def getOsPathSeparator(self) -> str:
        pass

    @abc.abstractmethod
    def getPathApp(self,path: str) -> str:
        pass

    @abc.abstractmethod
    def createFile(self, fileDto: FileDTO) -> str:
        pass