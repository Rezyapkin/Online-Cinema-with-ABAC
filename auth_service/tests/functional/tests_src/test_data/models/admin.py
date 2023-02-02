from pydantic import BaseModel


class UserRequest(BaseModel):
    user_id: str


class UserResponse(BaseModel):
    email: str
    id: str
    is_active: bool
    is_superuser: bool


class UserListRequest(BaseModel):
    limit: int
    offset: int
