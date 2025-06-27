import abc

class ICredentials(abc.ABC):

    @abc.abstractmethod
    def getCredentials(scopesUrl, pathCredentials: str, pathToken: str):
        pass