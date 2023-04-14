class ConvertError(Exception):
    def __init__(self):
        self.message = 'Posted file is corrupted'


class ForbiddenExt(Exception):
    def __init__(self):
        self.message = 'Posted file has an unsupported ext'