from flasgger import Schema, fields


class CurrentUserOAuthAccount(Schema):
    provider = fields.Str(required=True)
    account_id = fields.Str(required=True)


class CurrentUserInfoResponseSchema(Schema):
    email = fields.Email(required=True)
    oauth_accounts = fields.Nested(CurrentUserOAuthAccount, many=True, required=True)
