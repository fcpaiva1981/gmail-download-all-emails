
class EmailBodyDTO:

    def __init__(self, mime_type,  txt, html, others, errors):
        self.mime_type = mime_type
        self.txt = txt
        self.html = html
        self.others = others
        self.errors = errors