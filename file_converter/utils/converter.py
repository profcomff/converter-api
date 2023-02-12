from os.path import abspath
import aiofiles
from fastapi.exceptions import HTTPException
from file_converter.utils.commands import run
import hashlib
import random


def randomStr(n):
    alph="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    s=""
    for i in range (n):
        s+=alph[random.randint(0,len(alph)-1)]
    return s

async def convert(file, ext, settings):
    memory_file = await file.read()
    name = hashlib.sha512(memory_file).hexdigest()+randomStr(10)+"."+ext
    path =  abspath(settings.STATIC_FOLDER) + '/' + name
    async with aiofiles.open(path, 'wb') as saved_file:
        if len(memory_file) > settings.MAX_SIZE:
            raise HTTPException(415, f'File too large, {settings.MAX_SIZE} bytes allowed')
        await saved_file.write(memory_file)
    await file.close()
    await run (f"libreoffice --headless --convert-to {ext} {name}")
    return [f"{name}.{ext}",path]