from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class CreateUserRequest(_message.Message):
    __slots__ = ["email", "password"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class CreateUserResponse(_message.Message):
    __slots__ = ["email", "id"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    email: str
    id: str
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class GetUserLoginHistoryRequest(_message.Message):
    __slots__ = ["access_token", "page_number", "page_size"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PAGE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    page_number: int
    page_size: int
    def __init__(
        self, access_token: _Optional[str] = ..., page_number: _Optional[int] = ..., page_size: _Optional[int] = ...
    ) -> None: ...

class GetUserLoginHistoryResponse(_message.Message):
    __slots__ = ["next_page", "prev_page", "results", "total_count", "total_pages"]
    NEXT_PAGE_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    next_page: int
    prev_page: int
    results: _containers.RepeatedCompositeFieldContainer[UserLoginHistory]
    total_count: int
    total_pages: int
    def __init__(
        self,
        results: _Optional[_Iterable[_Union[UserLoginHistory, _Mapping]]] = ...,
        total_count: _Optional[int] = ...,
        total_pages: _Optional[int] = ...,
        prev_page: _Optional[int] = ...,
        next_page: _Optional[int] = ...,
    ) -> None: ...

class GetUserMeRequest(_message.Message):
    __slots__ = ["access_token"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    def __init__(self, access_token: _Optional[str] = ...) -> None: ...

class GetUserMeResponse(_message.Message):
    __slots__ = ["email", "oauth_accounts"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    OAUTH_ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    email: str
    oauth_accounts: _containers.RepeatedCompositeFieldContainer[UserOAuthProviderAccount]
    def __init__(
        self,
        email: _Optional[str] = ...,
        oauth_accounts: _Optional[_Iterable[_Union[UserOAuthProviderAccount, _Mapping]]] = ...,
    ) -> None: ...

class UserLoginHistory(_message.Message):
    __slots__ = ["date", "device", "ip_address", "user_agent"]
    DATE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    date: str
    device: str
    ip_address: str
    user_agent: str
    def __init__(
        self,
        date: _Optional[str] = ...,
        ip_address: _Optional[str] = ...,
        user_agent: _Optional[str] = ...,
        device: _Optional[str] = ...,
    ) -> None: ...

class UserOAuthProviderAccount(_message.Message):
    __slots__ = ["account_id", "provider"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    provider: str
    def __init__(self, provider: _Optional[str] = ..., account_id: _Optional[str] = ...) -> None: ...
