import abc

from src.dto.FormatedDateDTO import FormatedDateDTO


class IUtilsFunctions(abc.ABC):

    @abc.abstractmethod
    def formatDate(self, date: str) -> FormatedDateDTO:
        pass

    @abc.abstractmethod
    def jsonSerializer(self, obj) -> str:
        pass

    @abc.abstractmethod
    def jsonDumps(self, obj) -> str:
        pass

