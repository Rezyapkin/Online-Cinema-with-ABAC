from models.base import BaseOrjsonModel


class OAuth2TokensResponse(BaseOrjsonModel):
    token_type: str
    access_token: str
    expires_in: int


class OpenIdOAuth2TokensResponse(OAuth2TokensResponse):
    id_token: str
