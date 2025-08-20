from . import documents
from file_converter.converters.pandoc_documents import PandocOdt, PandocRtf


# Make additional converters available with proper class names
class Odt(PandocOdt):
    pass


class Rtf(PandocRtf):
    pass


__all__ = ['documents', 'Odt', 'Rtf']
