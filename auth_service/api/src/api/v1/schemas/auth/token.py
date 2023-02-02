from flasgger import Schema, fields


class Token(Schema):
    access_token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)
    token_type = fields.Str(required=True)
    expires_in = fields.Int(required=True)
