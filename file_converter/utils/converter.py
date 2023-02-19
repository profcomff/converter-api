import aiofiles
from file_converter.utils.commands import run
import random
from PyPDF3 import PdfFileReader
from PyPDF3.utils import PyPdfError
import io
from os.path import splitext
import string
import time

def randomStr(n):
    alph =  string.ascii_letters
    s = ""
    for i in range(n):
        s += alph[random.randint(0, len(alph) - 1)]
    return s


async def convert(file, ext, settings):
    memory_file = await file.read()
    name = str(time.time())+"_"+randomStr(10) + "." + "doc" 
    print(name)
    path = settings.STATIC_FOLDER + '/' + name
    async with aiofiles.open(path, 'wb') as saved_file:
        await saved_file.write(memory_file)
    await file.close()
    fileName, extension = splitext(path)  # [0] - путь + имя, [1] - расширение
    extension = extension.lower()
    if not ext == extension:
        pass
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

