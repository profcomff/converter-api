import aiofiles
from file_converter.utils.commands import run
import random
from PyPDF3 import PdfFileReader
from PyPDF3.utils import PyPdfError
import io
from os.path import splitext
import string
import time
from fastapi import File
from os.path import exists


async def convert_doc_pdf(file_name: str):
    await run(f"cd static; libreoffice --headless --convert-to pdf {file_name}")


async def convert_docx_pdf(file_name: str):
    await run(f"cd static; libreoffice --headless --convert-to pdf {file_name}")


convert_runnables = {"doc_pdf": convert_doc_pdf, "docx_pdf": convert_docx_pdf}


def randomStr(n):
    alph = string.ascii_letters
    s = ""
    for i in range(n):
        s += alph[random.randint(0, len(alph) - 1)]
    return s


async def convert(file: File, ext: str, static_folder: str):
    memory_file = await file.read()
    name = str(time.time()) + "_" + randomStr(10) + "." + splitext(file.filename)[1].replace('.', '')
    path = static_folder + '/' + name
    async with aiofiles.open(path, 'wb') as saved_file:
        await saved_file.write(memory_file)
    await file.close()
    fileName, extension = splitext(path)  # [0] - путь + имя, [1] - расширение
    extension = extension.lower()
    if not ext == extension:
        await convert_runnables[extension[1:] + "_" + ext](name)
        await run(f"rm static/{name} ")
    return f"{fileName}.{ext}"


async def check_pdf_ok(fullfile: str):
    if not exists(fullfile):
        return False
    async with aiofiles.open(fullfile, 'rb') as f:
        try:
            f = await f.read()
            pdf = PdfFileReader(io.BytesIO(f))
            info = pdf.getDocumentInfo()
            return bool(info)
        except PyPdfError:
            return False
