"""
All Rules that are related to comparison operators: ==, !=, <, >, <=, >=
"""

from abc import ABC
from typing import Any, Literal

from ..rules.base import Rule


class OperatorRule(Rule, ABC):
    """
    Base class for all Logic Operator Rules
    """

    value: Any


class Eq(OperatorRule):
    """
    Rule that is satisfied when two values are equal '=='.
    For example:
        Policy: subjects={'name': Eq(value='max'}}
        Example in Inquiry: subjects={'name': 'Max'	}
    """

    rule_type: Literal["Eq"] = "Eq"

    def satisfied(self, what: Any, inquiry: None = None) -> bool:
        if isinstance(self.value, tuple):
            val = list(self.value)
        else:
            val = self.value

        return val == what


class NotEq(OperatorRule):
    """
    Rule that is satisfied when two values are not equal '!='.
    For example:
        Policy: subjects={'age': NotEq(value=40)}
        Example in Inquiry: subjects={'age': '40'}
    """

    rule_type: Literal["NotEq"] = "NotEq"

    def satisfied(self, what: Any, inquiry: None = None) -> bool:
        if isinstance(self.value, tuple):
            val = list(self.value)
        else:
            val = self.value

        return val != what


class Greater(OperatorRule):
    """
    Rule that is satisfied when 'what' is greater '>' than initial value.
    For example:
        Policy: subjects={'age': Greater(value=40.2)}
        Example in Inquiry: subjects={'age': '40.3'}
    """

    rule_type: Literal["Greater"] = "Greater"

    def satisfied(self, what: Any, inquiry: None = None) -> bool:
        return what > self.value


class Less(OperatorRule):
    """
    Rule that is satisfied when 'what' is less '<' than initial value.
    For example:
        Policy: subjects={'age': Less(value=40.2)}
        Example in Inquiry: subjects={'age': '40.1'}
    """

    rule_type: Literal["Less"] = "Less"

    def satisfied(self, what: Any, inquiry: None = None) -> bool:
        return what < self.value


class GreaterOrEqual(OperatorRule):
    """
    Rule that is satisfied when 'what' is greater or equal '>=' than initial value.
    For example:
        Policy: subjects={'age': GreaterOrEqual(value=40.2)}
        Example in Inquiry: subjects={'age': '40.2'}
    """

    rule_type: Literal["GreaterOrEqual"] = "GreaterOrEqual"

    def satisfied(self, what: Any, inquiry: None = None) -> bool:
        return what >= self.value


class LessOrEqual(OperatorRule):
    """
    Rule that is satisfied when 'what' is less or equal '<=' than initial value.
    For example:
        Policy: subjects={'age': LessOrEqual(value=40.2)}
        Example in Inquiry: subjects={'age': '40.2'}
    """

    rule_type: Literal["GreaterOrEqual"] = "GreaterOrEqual"

    def satisfied(self, what: Any, inquiry: None = None) -> bool:
        return what <= self.value
