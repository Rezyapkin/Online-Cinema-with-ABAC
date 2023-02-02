from flasgger import Schema, fields


class ErrorResponse(Schema):
    description = fields.Str(required=True)
