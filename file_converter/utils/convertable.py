from __future__ import annotations
import aiofiles
from file_converter.utils.commands import run
from file_converter.utils.random_str import random_str
import time
from fastapi import File, HTTPException
from abc import ABCMeta, abstractmethod
import re
import os
from get_dir import get_command

SUPPORTED_TYPES: list[str] = []
TYPES: dict[str, type[Convertable]] = dict()


class GetCommand:

    direct: str
    command: str
    def __init__(self, filename: str):
        _com = get_command(filename)
        self.command = _com.get('command')
        self.direct = _com.get('direct')


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
    def convert(command: str):
        raise NotImplementedError()


class Doc(Convertable):
    @staticmethod
    async def convert(command: str):
        await run(command)


class Docx(Convertable):
    @staticmethod
    async def convert(command: str):
        await run(command)


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
            await TYPES[extension].convert(get.command)  # Ищем по расширению метод для конвертации
        except KeyError:
            raise HTTPException(415, 'unsupported to_ext')
        os.remove(get.direct)  # Удаляет старый файл, до конвертации
    return f"{file_name}.{ext}"
