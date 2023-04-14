from __future__ import annotations

from typing import Callable, Awaitable

from file_converter.converters.convertable import Convertable
from file_converter.utils.libre import get_command


class Doc(Convertable):
    _com: Callable[[str, str], Awaitable[None]] = get_command()

    @classmethod
    async def convert(mcs, file_name: str, _new_filename: str):
        await mcs._com(file_name, _new_filename)


class Docx(Convertable):
    _com: Callable[[str, str], Awaitable[None]] = get_command()

    @classmethod
    async def convert(mcs, file_name: str, _new_filename: str):
        await mcs._com(file_name, _new_filename)
