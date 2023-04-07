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
from get_dir import cd, slash, command

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
    def convert(file_name: str):
        raise NotImplementedError()


class Doc(Convertable):
    @staticmethod
    async def convert(file_name: str):
        await run(f"cd {cd}{command}{file_name}")


class Docx(Convertable):
    @staticmethod
    async def convert(file_name: str):
        await run(f"cd {cd}{command}{file_name}")


def random_str(n):
    alph = string.ascii_letters
    return ''.join(random.choice(alph) for i in range(n))


async def convert(file: File, ext: str, static_folder: str):
    memory_file = await file.read()
    name = str(time.time()) + "_" + random_str(10) + "." + file.filename.split('.')[-1].replace('.', '')
    path = static_folder + slash + name

    async with aiofiles.open(path, 'wb') as saved_file:
        await saved_file.write(memory_file)
    await file.close()

    extension = path.split(".")[-1]
    file_name = path[0:-len(extension)-1]
    extension = extension.lower()  # убрать точку перед расширением
    if not ext == extension:
        try:
            await TYPES[extension].convert(name)
        except KeyError:
            raise HTTPException(415, 'unsupported to_ext')
        os.remove(f"{cd}{name}")
    return f"{file_name}.{ext}"
