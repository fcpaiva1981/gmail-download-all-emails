from src.services.OSDirectoriesFiles import OSDirectoriesFiles

class EnvsDTO:

    def __init__(self, scopesUrl, path_credentials , path_token , path_output_data):
        self.scopesUrl = [scopesUrl]
        self.path_credentials = path_credentials
        self.path_token = path_token
        self.path_output_data = path_output_data
        self.osUtils = OSDirectoriesFiles()

    def fixPaths(self):
        self.path_credentials =  self.osDirectoriesFiles.transformEnvPropInPath(self.path_credentials)
        self.path_token =  self.osDirectoriesFiles.transformEnvPropInPath(self.path_token)
        self.path_output_data =  self.osDirectoriesFiles.transformEnvPropInPath(self.path_output_data)
