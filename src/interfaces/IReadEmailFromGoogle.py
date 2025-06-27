import abc

from src.dto.EmailBodyDTO import EmailBodyDTO
from src.dto.EmailDataDTO import EmailDataDTO
from src.dto.EmailParserDTO import EmailParserDTO
from src.dto.HeadersDTO import HeadersDTO


class IReadEmailFromGoogle(abc.ABC):

    @abc.abstractmethod
    def get_email_body(self, payload) -> EmailBodyDTO:
        pass

    @abc.abstractmethod
    def get_email_headers(self, headers) -> HeadersDTO:
        pass

    @abc.abstractmethod
    def pars_email(self, payload, id_message) -> EmailParserDTO:
        pass

    @abc.abstractmethod
    def show_email_data(self, emailData: EmailDataDTO):
        pass