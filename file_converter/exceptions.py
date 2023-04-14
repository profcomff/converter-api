class ConvertError(Exception):
    def __init__(self):
        super().__init__('Posted file is corrupted')


class Unsupported_to_ext(Exception):
    def __init__(self):
        super().__init__('Unsupported to_ext')


class ForbiddenExt(Exception):
    def __init__(self):
        super().__init__('Unsupported ext')