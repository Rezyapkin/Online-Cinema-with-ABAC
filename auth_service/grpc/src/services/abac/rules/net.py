"""
All Rules relevant to networking context
"""

import ipaddress
from typing import Literal

from loguru import logger

from ..rules.base import Rule


class CIDR(Rule):
    """
    Rule that is satisfied when inquiry's IP address is in the provided CIDR.
    For example:
        Policy: context={'ip': CIDR(cidr='127.0.0.1/32')}
        Example in Inquiry:  context={'ip': '127.0.0.2'}
    """

    rule_type: Literal["CIDR"] = "CIDR"
    cidr: str

    def satisfied(self, what: str, inquiry: None = None) -> bool:
        if not isinstance(what, str):
            return False

        try:
            ip = ipaddress.ip_address(what)
            net = ipaddress.ip_network(self.cidr)
        except ValueError:
            logger.exception("Error {} satisfied", type(self).__name__)
            return False

        return ip in net
