import abc

from src.dto.EmailBodyDTO import EmailBodyDTO
from src.dto.EmailDataDTO import EmailDataDTO
from src.dto.HeadersDTO import HeadersDTO


class IReadEmailFromGoogle(abc.ABC):

    @abc.abstractmethod
    def getEmailBody(self, payload) -> EmailBodyDTO:
        pass

    @abc.abstractmethod
    def getEmailHeaders(self, headers) -> HeadersDTO:
        pass

    @abc.abstractmethod
    def parseEmail(self, payload, id_message):
        pass

    @abc.abstractmethod
    def showEmailData(self, emailData: EmailDataDTO):
        pass