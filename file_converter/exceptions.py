class HTTP_400_BAD_REQUEST(Exception):
    def __init__(self):
        self.message = 'Posted file is corrupted'

    def __str__(self):
        return f'{self.message}'

