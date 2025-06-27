import abc

from src.dto.EmailBodyDTO import EmailBodyDTO
from src.dto.HeadersDTO import HeadersDTO


class IReadEmailFromGoogle(abc.ABC):

    @abc.abstractmethod
    def getEmailBody(payload) -> EmailBodyDTO:
        pass

    @abc.abstractmethod
    def getEmailHeaders(self, headers) -> HeadersDTO:
        pass