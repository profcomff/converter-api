from PyPDF4 import PdfFileReader
import io
from os.path import exists

async def check_pdf_ok(full_file: str):
    if not exists(full_file):
        return False
    f = open(full_file, "rb").read()
    try:
        PdfFileReader(io.BytesIO(f))
        return True
    except Exception as e:
        return False
