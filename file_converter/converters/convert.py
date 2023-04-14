from __future__ import annotations

import time
import aiofiles
from fastapi import UploadFile
from file_converter.converters.convertable import settings, TYPES
from file_converter.utils.random_str import random_str
from file_converter.exceptions import ForbiddenExt, Unsupported_to_ext


async def convert(file: UploadFile, to_ext: str):

    if file.filename.split(".")[-1] not in settings.EXTENTIONS:
        raise ForbiddenExt()
    if to_ext not in settings.CONVERT_TYPES:
        raise Unsupported_to_ext()

    try:
        memory_file = await file.read()
        extension = file.filename.split(".")[-1]
    finally:
        await file.close()

    timestamp = str(time.time())
    _random_str = random_str(10)
    _old_name = f'{timestamp}_{_random_str}.{extension}'
    _old_path = f'{settings.STATIC_FOLDER}/{_old_name}'
    _new_name = f'{timestamp}_{_random_str}.{to_ext}'

    async with aiofiles.open(_old_path, 'wb') as saved_file:
        await saved_file.write(memory_file)  # Сохраняем пришедший файл

    extension = extension.lower()  # Убрать точку перед расширением
    await TYPES[extension].convert(_old_name, _new_name)

    return _new_name
