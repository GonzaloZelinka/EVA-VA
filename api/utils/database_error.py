from api.config import Config


class ToDatabaseException(Exception):
    def __init__(self, message, details, code):
        self.message = message
        self.details = details
        self.code = code

    def to_dict(self):
        return {
            "message": self.message,
            "details": self.details,
            "code": self.code,
        }
