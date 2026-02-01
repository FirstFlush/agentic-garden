from typing import Protocol
from datetime import datetime


class HasCreated(Protocol):

    @property
    def created(self) -> datetime:
        ...
