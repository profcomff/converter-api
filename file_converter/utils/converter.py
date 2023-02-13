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

# libs for image converting
'''
from PIL import Image
from fpdf import FPDF
'''


def randomStr(n):
    alph = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    s = ""
    for i in range(n):
        s += alph[random.randint(0, len(alph) - 1)]
    return s


async def convert(file, ext, settings):
    memory_file = await file.read()
    name = hashlib.sha512(memory_file).hexdigest() + randomStr(10) + "." + ext
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


async def check_pdf_ok(fullfile:str):
    async with aiofiles.open(fullfile, 'rb') as f:
        try:
            f = await f.read()
            pdf = PdfFileReader(io.BytesIO(f))
            info = pdf.getDocumentInfo()
            return bool(info)
        except PyPdfError:
            return False

'''
#преобразует файл из картинки в pdf
async def process_image(file :str,newFileName :str):
    async with Image.open(BytesIO(file)).convert("RGB")  as img:
        if(img.width>img.height):
            img=await img.rotate(90,expand=True)
        pdf = FPDF()
        pdf.add_page()

        FPDF.set_left_margin(pdf,0)
        FPDF.set_right_margin(pdf,0)
        FPDF.set_top_margin(pdf,10)
    
        k=min(pdf.eph/img.height,pdf.epw/img.width)
        wid=img.width*k
        heig=img.height*k
        await pdf.image(img, x=(pdf.epw-wid)/2,y=(pdf.eph-heig)/2+15,h=heig, w=wid) 
        await pdf.output(f"{newFileName}.pdf")
'''
