from __future__ import annotations

from typing import Awaitable, Callable

from file_converter.converters.convertable import Convertable
from file_converter.utils.pandoc import get_pandoc_command


class PandocDoc(Convertable):
    """Document converter using Pandoc - supports .doc files"""
    _com: Callable[[str, str], Awaitable[None]] = get_pandoc_command()

    @classmethod
    async def convert(mcs, file_name: str, _new_filename: str):
        await mcs._com(file_name, _new_filename)


class PandocDocx(Convertable):
    """Document converter using Pandoc - supports .docx files"""
    _com: Callable[[str, str], Awaitable[None]] = get_pandoc_command()

    @classmethod
    async def convert(mcs, file_name: str, _new_filename: str):
        await mcs._com(file_name, _new_filename)


class PandocOdt(Convertable):
    """OpenDocument Text converter using Pandoc - supports .odt files"""
    _com: Callable[[str, str], Awaitable[None]] = get_pandoc_command()

    @classmethod
    async def convert(mcs, file_name: str, _new_filename: str):
        await mcs._com(file_name, _new_filename)


class PandocRtf(Convertable):
    """Rich Text Format converter using Pandoc - supports .rtf files"""
    _com: Callable[[str, str], Awaitable[None]] = get_pandoc_command()

    @classmethod
    async def convert(mcs, file_name: str, _new_filename: str):
        await mcs._com(file_name, _new_filename)