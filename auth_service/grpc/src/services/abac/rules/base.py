"""
Base Rule. Should be extended be concrete ones.
"""

from abc import ABC, abstractmethod
from typing import Any, Literal

from ..guard import Inquiry
from ..utils import BaseOrjsonModel, PrettyPrint


class Rule(BaseOrjsonModel, PrettyPrint, ABC):
    """Basic Rule"""

    rule_type: Literal["Rule"]

    @abstractmethod
    def satisfied(self, what: Any, inquiry: Inquiry | None = None) -> bool:
        """Is rule satisfied by the inquiry"""
        pass
