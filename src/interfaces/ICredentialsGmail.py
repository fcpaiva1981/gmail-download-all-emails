import abc

class ICredentialsGmail(abc.ABC):

    @abc.abstractmethod
    def getCredentials(self):
        pass
