from __future__ import annotations

import time

import aiofiles
from fastapi import UploadFile

from file_converter.converters.convertable import TYPES, settings
from file_converter.exceptions import EqualExtensions, ForbiddenExt, UnsupportedToExt
from file_converter.utils.random_str import random_str


async def convert(file: UploadFile, to_ext: str):
    if file.filename.split(".")[-1] not in settings.EXTENTIONS:
        raise ForbiddenExt()
    if to_ext not in settings.CONVERT_TYPES:
        raise UnsupportedToExt()

    try:
        memory_file = await file.read()
        extension = file.filename.split(".")[-1]
    finally:
        await file.close()
    if extension == to_ext:
        raise EqualExtensions()

    timestamp = str(time.time())
    _random_str = random_str(10)
    _old_name = f'{timestamp}_{_random_str}.{extension}'
    _old_path = f'{settings.STATIC_FOLDER}/{_old_name}'
    _new_name = f'{timestamp}_{_random_str}.{to_ext}'

    async with aiofiles.open(_old_path, 'wb') as saved_file:
        await saved_file.write(memory_file)  # Сохраняем пришедший файл

    extension = extension.lower()
    await TYPES[extension].convert(_old_name, _new_name)

    return _new_name
