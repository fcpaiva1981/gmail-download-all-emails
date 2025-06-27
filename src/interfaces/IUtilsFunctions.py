import abc

from src.dto.FormatedDateDTO import FormatedDateDTO


class IUtilsFunctions(abc.ABC):

    @abc.abstractmethod
    def format_date(self, date: str) -> FormatedDateDTO:
        pass

    @abc.abstractmethod
    def json_serializer(self, obj) -> str:
        pass

    @abc.abstractmethod
    def json_dmps(self, obj) -> str:
        pass

