from __future__ import annotations
import aiofiles
from file_converter.utils.commands import run
import random
import string
import time
from fastapi import File, HTTPException
from abc import ABCMeta, abstractmethod
import re
import os
from get_dir import GetCommand

SUPPORTED_TYPES: list[str] = []
TYPES: dict[str, type[Convertable]] = dict()


class Convertable(ABCMeta):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        TYPES[cls.get_name()] = cls
        SUPPORTED_TYPES.append(cls.get_name())

    @classmethod
    def get_name(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

    @staticmethod
    @abstractmethod
    def convert(get: GetCommand):
        raise NotImplementedError()


class Doc(Convertable):
    @staticmethod
    async def convert(get: GetCommand):
        await run(get.command)


class Docx(Convertable):
    @staticmethod
    async def convert(get: GetCommand):
        await run(get.command)


def random_str(n):
    alph = string.ascii_letters
    return ''.join(random.choice(alph) for i in range(n))


async def convert(file: File, ext: str):
    memory_file = await file.read()
    name = str(time.time()) + "_" + random_str(10) + "." + file.filename.split('.')[-1].replace('.', '')
    get = GetCommand(name)
    path = get.direct

    async with aiofiles.open(path, 'wb') as saved_file:
        await saved_file.write(memory_file)  # Сохраняем пришедший файл
    await file.close()

    extension = path.split(".")[-1]
    file_name = path[0:-len(extension)-1]
    extension = extension.lower()  # Убрать точку перед расширением
    if not ext == extension:
        try:
            await TYPES[extension].convert(get)  # Ищем по расширению метод для конвертации
        except KeyError:
            raise HTTPException(415, 'unsupported to_ext')
        os.remove(get.direct)  # Удаляет старый файл, до конвертации
    return f"{file_name}.{ext}"
