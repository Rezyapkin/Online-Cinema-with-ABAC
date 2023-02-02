from email_validator import validate_email, EmailNotValidError
from pydantic import Field, validator


from models.base import BaseOrjsonModel


class OAuthAccount(BaseOrjsonModel):
    id: str
    email: str = Field(..., min_length=1)

    @validator("email")
    def validate_email(cls, v):  # noqa: N805
        try:
            validate_email(v, check_deliverability=False)
        except EmailNotValidError:
            raise ValueError("not valid email")

        return v
