from flasgger import Schema, fields


class IdSchema(Schema):
    id = fields.Str(required=True)
