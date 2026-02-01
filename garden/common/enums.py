from enum import Enum, EnumMeta
from typing import Any


class GardenEnumMeta(EnumMeta):

    @property
    def values(cls) -> list[Any]:
        return [enum.value for _, enum in cls.__members__.items()] # type: ignore

    @property
    def choices(cls) -> list[tuple[Any, Any]]:
        return [(enum.value, enum.value) for enum in cls] # type: ignore


class GardenEnum(Enum, metaclass=GardenEnumMeta):
    pass