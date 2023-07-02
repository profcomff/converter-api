class ConvertError(Exception):
    def __init__(self):
        super().__init__('Posted file is corrupted')


class UnsupportedToExt(Exception):
    def __init__(self):
        super().__init__('Unsupported to_ext')


class ForbiddenExt(Exception):
    def __init__(self):
        super().__init__('Unsupported ext')


class EqualExtensions(Exception):
    def __init__(self):
        super().__init__('File extension is equals to "to_ext"')
