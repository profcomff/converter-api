from __future__ import annotations

import re
from abc import ABCMeta, abstractmethod

from file_converter.settings import get_settings


settings = get_settings()
SUPPORTED_TYPES: list[str] = []
TYPES: dict[str, type[Convertable]] = dict()


class Convertable(ABCMeta):
    def __init_subclass__(mcs, **kwargs):
        super().__init_subclass__(**kwargs)
        TYPES[mcs.get_name()] = mcs
        SUPPORTED_TYPES.append(mcs.get_name())

    @classmethod
    def get_name(mcs) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", mcs.__name__).lower()

    @classmethod
    @abstractmethod
    def convert(mcs, file_name: str, _new_filename: str):
        raise NotImplementedError()
