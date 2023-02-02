from dataclasses import dataclass


@dataclass
class LogInRequest:
    email: str
    password: str
    ip: str
    user_agent: str
