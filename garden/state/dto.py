from datetime import datetime
from typing import TypedDict


class EvidenceWindow(TypedDict):
    window_start: datetime
    window_end: datetime
    sample_count: int
