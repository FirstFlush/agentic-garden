from enum import Enum, EnumMeta
from typing import Any


class GardenEnumMeta(EnumMeta):

    @property
    def values(cls) -> list[Any]:
        return [enum.value for _, enum in cls.__members__.items()] # type: ignore


class GardenEnum(Enum, metaclass=GardenEnumMeta):
    pass