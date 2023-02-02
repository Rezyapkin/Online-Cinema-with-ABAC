from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AttachAccountToUserRequest(_message.Message):
    __slots__ = ["access_token", "code", "state_token"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    STATE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    code: str
    state_token: str
    def __init__(
        self, access_token: _Optional[str] = ..., code: _Optional[str] = ..., state_token: _Optional[str] = ...
    ) -> None: ...

class AttachAccountToUserResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DetachAccountFromUserRequest(_message.Message):
    __slots__ = ["access_token"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    def __init__(self, access_token: _Optional[str] = ...) -> None: ...

class DetachAccountFromUserResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetProviderLoginURLRequest(_message.Message):
    __slots__ = ["access_token", "callback_url"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CALLBACK_URL_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    callback_url: str
    def __init__(self, callback_url: _Optional[str] = ..., access_token: _Optional[str] = ...) -> None: ...

class GetProviderLoginURLResponse(_message.Message):
    __slots__ = ["state_token", "url"]
    STATE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    state_token: str
    url: str
    def __init__(self, url: _Optional[str] = ..., state_token: _Optional[str] = ...) -> None: ...

class OAuthLoginRequest(_message.Message):
    __slots__ = ["code", "state_token"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    STATE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    code: str
    state_token: str
    def __init__(self, code: _Optional[str] = ..., state_token: _Optional[str] = ...) -> None: ...

class OAuthLoginResponse(_message.Message):
    __slots__ = ["access_token", "expires_in", "refresh_token", "token_type"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_IN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    expires_in: int
    refresh_token: str
    token_type: str
    def __init__(
        self,
        access_token: _Optional[str] = ...,
        refresh_token: _Optional[str] = ...,
        expires_in: _Optional[int] = ...,
        token_type: _Optional[str] = ...,
    ) -> None: ...
