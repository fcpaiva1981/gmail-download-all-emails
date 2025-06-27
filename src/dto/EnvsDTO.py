class EnvsDTO:

    def __init__(self, scopesUrl, path_credentials , path_token , path_output_data, show_body):
        self.scopesUrl = [scopesUrl]
        self.path_credentials = path_credentials
        self.path_token = path_token
        self.path_output_data = path_output_data
        self.show_body = show_body
