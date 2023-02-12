from os.path import abspath, exists
import aiofiles
import aiofiles.os
from file_converter.settings import Settings, get_settings


async def convert(file,ext):
    path =  path = abspath(settings.STATIC_FOLDER) + '/' + "test"

    async with aiofiles.open(path, 'wb') as saved_file:
        memory_file = await file.read()
        if len(memory_file) > settings.MAX_SIZE:
            raise HTTPException(415, f'File too large, {settings.MAX_SIZE} bytes allowed')
        await saved_file.write(memory_file)
    await file.close()
