class NotFoundException(Exception):
    def __init__(self, msg: str, details: list = None):
        self.msg = msg
        self.details = details

class InternalServerException(Exception):
    def __init__(self, msg: str, details: list = None):
        self.msg = msg
        self.details = details

class BadRequestException(Exception):
    def __init__(self, msg: str, details: list = None):
        self.msg = msg
        self.details = details