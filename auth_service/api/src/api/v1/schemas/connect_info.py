from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address


@dataclass
class ConnectionInfo:
    user_ip: IPv4Address | IPv6Address
    user_agent: str
