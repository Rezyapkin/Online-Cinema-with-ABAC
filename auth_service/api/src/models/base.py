from dataclasses import dataclass, fields
from typing import Any


@dataclass
class BasePagination:
    total_count: int
    total_pages: int
    prev_page: int | None
    next_page: int | None

    @classmethod
    def instance_from(cls, obj: Any):
        params = {field.name: getattr(obj, field.name) for field in fields(cls) if hasattr(obj, field.name)}
        return cls(**params)
