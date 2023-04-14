class ConvertError(Exception):
    def __init__(self):
        super().__init__('Posted file is corrupted')


class UnsupportedtoExt(Exception):
    def __init__(self):
        super().__init__('Unsupported to_ext')


class ForbiddenExt(Exception):
    def __init__(self):
        super().__init__('Unsupported ext')
