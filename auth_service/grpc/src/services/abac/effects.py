"""
Effect constants.
"""
from enum import Enum


class Effects(str, Enum):
    # AllowAccess is an effect for policies that allow access.
    ALLOW_ACCESS: str = "allow"
    # DenyAccess is an effect for policies that deny access.
    DENY_ACCESS: str = "deny"
