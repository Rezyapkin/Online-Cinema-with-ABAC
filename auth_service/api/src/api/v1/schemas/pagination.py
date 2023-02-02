from dataclasses import dataclass

from flasgger import Schema, fields
from marshmallow import validate


@dataclass
class RequestWithPagination:
    page_number: int
    page_size: int


class PaginationSchema(Schema):
    page_number = fields.Integer(
        required=True, validate=validate.Range(min=1, min_inclusive=True, error="'page_number' must be bigger than 0")
    )
    page_size = fields.Integer(
        required=True, validate=validate.Range(min=0, error="'page_size' must be be bigger non-negative")
    )


class PaginationResponseSchema(Schema):
    total_count = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    prev_page = fields.Integer()
    next_page = fields.Integer()
