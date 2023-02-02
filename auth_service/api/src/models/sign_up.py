from dataclasses import dataclass


@dataclass
class SignUpRequest:
    email: str
    password: str
    ip: str
    user_agent: str


@dataclass
class SignUpResponse:
    email: str
    id: str
