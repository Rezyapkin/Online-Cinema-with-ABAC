from pydantic import validator, Field

from models.base import BaseOrjsonModel


class BasePaginationResultDto(BaseOrjsonModel):
    total_count: int
    total_pages: int
    prev_page: int | None
    next_page: int | None

    @staticmethod
    def create(total_count: int, page_number: int, page_size: int) -> dict[str, int | None]:
        total_pages = total_count // page_size + (1 if total_count % page_size else 0)
        prev_page = number if (number := page_number - 1) > 0 and number <= total_pages else None
        next_page = number if (number := page_number + 1) <= total_pages else None
        return {"total_count": total_count, "total_pages": total_pages, "prev_page": prev_page, "next_page": next_page}


class LimitOffsetModel(BaseOrjsonModel):
    limit: int
    offset: int


class BasePaginationEntryDto(BaseOrjsonModel):
    page_number: int = Field(..., gt=0)
    page_size: int

    def get_limit_offset(self) -> LimitOffsetModel:
        offset = (self.page_number - 1) * self.page_size
        return LimitOffsetModel(limit=self.page_size, offset=offset)

    @validator("page_size")
    def default_limit(cls, v):  # noqa: N805
        if v < 0:
            raise ValueError("limit must be bigger then 0")

        if v == 0:  # (это дефолт, если не передать)
            v = 10
        return v
