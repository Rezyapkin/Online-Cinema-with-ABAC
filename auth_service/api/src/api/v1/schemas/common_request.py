from dataclasses import dataclass


@dataclass
class CommonRequest:
    token: str
    user_ip: str
    user_agent: str
