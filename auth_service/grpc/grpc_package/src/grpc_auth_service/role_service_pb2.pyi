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

class AnyUserOAuthProviderAccount(_message.Message):
    __slots__ = ["account_id", "provider"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    provider: str
    def __init__(self, provider: _Optional[str] = ..., account_id: _Optional[str] = ...) -> None: ...

class CheckAccessRequest(_message.Message):
    __slots__ = ["access_token", "inquiry"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    INQUIRY_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    inquiry: str
    def __init__(self, access_token: _Optional[str] = ..., inquiry: _Optional[str] = ...) -> None: ...

class CheckAccessResponse(_message.Message):
    __slots__ = ["has_access"]
    HAS_ACCESS_FIELD_NUMBER: _ClassVar[int]
    has_access: bool
    def __init__(self, has_access: bool = ...) -> None: ...

class CreatePolicyRequest(_message.Message):
    __slots__ = ["access_token", "policy"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    policy: str
    def __init__(self, access_token: _Optional[str] = ..., policy: _Optional[str] = ...) -> None: ...

class CreatePolicyResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeletePolicyRequest(_message.Message):
    __slots__ = ["access_token", "id"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    id: str
    def __init__(self, access_token: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class DeletePolicyResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetPolicyListRequest(_message.Message):
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

class GetPolicyListResponse(_message.Message):
    __slots__ = ["next_page", "policy", "prev_page", "total_count", "total_pages"]
    NEXT_PAGE_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    next_page: int
    policy: _containers.RepeatedScalarFieldContainer[str]
    prev_page: int
    total_count: int
    total_pages: int
    def __init__(
        self,
        policy: _Optional[_Iterable[str]] = ...,
        total_count: _Optional[int] = ...,
        total_pages: _Optional[int] = ...,
        prev_page: _Optional[int] = ...,
        next_page: _Optional[int] = ...,
    ) -> None: ...

class GetPolicyRequest(_message.Message):
    __slots__ = ["access_token", "id"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    id: str
    def __init__(self, access_token: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class GetPolicyResponse(_message.Message):
    __slots__ = ["policy"]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: str
    def __init__(self, policy: _Optional[str] = ...) -> None: ...

class GetUserListRequest(_message.Message):
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

class GetUserListResponse(_message.Message):
    __slots__ = ["next_page", "prev_page", "results", "total_count", "total_pages"]
    NEXT_PAGE_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    next_page: int
    prev_page: int
    results: _containers.RepeatedCompositeFieldContainer[UserInList]
    total_count: int
    total_pages: int
    def __init__(
        self,
        results: _Optional[_Iterable[_Union[UserInList, _Mapping]]] = ...,
        total_count: _Optional[int] = ...,
        total_pages: _Optional[int] = ...,
        prev_page: _Optional[int] = ...,
        next_page: _Optional[int] = ...,
    ) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ["access_token", "id"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    id: str
    def __init__(self, access_token: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ["email", "id", "is_active", "is_superuser", "oauth_accounts"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    IS_SUPERUSER_FIELD_NUMBER: _ClassVar[int]
    OAUTH_ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    email: str
    id: str
    is_active: bool
    is_superuser: bool
    oauth_accounts: _containers.RepeatedCompositeFieldContainer[AnyUserOAuthProviderAccount]
    def __init__(
        self,
        id: _Optional[str] = ...,
        email: _Optional[str] = ...,
        is_active: bool = ...,
        is_superuser: bool = ...,
        oauth_accounts: _Optional[_Iterable[_Union[AnyUserOAuthProviderAccount, _Mapping]]] = ...,
    ) -> None: ...

class UpdatePolicyRequest(_message.Message):
    __slots__ = ["access_token", "id", "policy"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    id: str
    policy: str
    def __init__(
        self, access_token: _Optional[str] = ..., id: _Optional[str] = ..., policy: _Optional[str] = ...
    ) -> None: ...

class UpdatePolicyResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UserInList(_message.Message):
    __slots__ = ["email", "id", "is_active", "is_superuser"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    IS_SUPERUSER_FIELD_NUMBER: _ClassVar[int]
    email: str
    id: str
    is_active: bool
    is_superuser: bool
    def __init__(
        self, id: _Optional[str] = ..., email: _Optional[str] = ..., is_active: bool = ..., is_superuser: bool = ...
    ) -> None: ...
