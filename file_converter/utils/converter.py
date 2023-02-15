from os.path import abspath
import aiofiles
from fastapi.exceptions import HTTPException
from file_converter.utils.commands import run
import hashlib
import random
from PyPDF3 import PdfFileReader
from PyPDF3.utils import PyPdfError
import io
from os.path import splitext
import string
import datetime

def randomStr(n):
    alph =  string.ascii_letters
    s = ""
    for i in range(n):
        s += alph[random.randint(0, len(alph) - 1)]
    return s


async def convert(file, ext, settings):
    memory_file = await file.read()
    name = str(datetime.datetime.now())+"#"+randomStr(10) + "." + ext
    path = abspath(settings.STATIC_FOLDER) + '/' + name
    async with aiofiles.open(path, 'wb') as saved_file:
        if len(memory_file) > settings.MAX_SIZE:
            raise HTTPException(415, f'File too large, {settings.MAX_SIZE} bytes allowed')
        await saved_file.write(memory_file)
    await file.close()
    fileName, extension = splitext(path)  # [0] - путь + имя, [1] - расширение
    extension = extension.lower()
    if not ext == extension:
        await run(f"libreoffice --headless --convert-to {ext} {name}")
    # await run (f"rm static/{name} ")
    return [f"{name}", path]


async def check_pdf_ok(fullfile: str):
    async with aiofiles.open(fullfile, 'rb') as f:
        try:
            f = await f.read()
            pdf = PdfFileReader(io.BytesIO(f))
            info = pdf.getDocumentInfo()
            return bool(info)
        except PyPdfError:
            return False

