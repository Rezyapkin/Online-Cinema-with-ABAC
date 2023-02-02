"""
All Rules relevant to list-related context.

Various search options are available:
- is item in list?
- is not item in the list?
- are all the items in the list?
- are all the items not in the list?
- is at least one of the provided items in the list?
- is at least one of the provided items not in the list?
"""

from abc import ABC
from typing import Iterable, Literal

from ..rules.base import Rule


class ListRule(Rule, ABC):
    """
    Generic Rule for List-related checks
    """

    data: set[str]

    @staticmethod
    def _one_in_list(what: str, data: set[str]) -> bool:
        return what in data

    @staticmethod
    def _all_in_list(what: Iterable[str], data: set[str]) -> bool:
        return set(what).issubset(data)

    @staticmethod
    def _any_in_list(what: Iterable[str], data: set[str]) -> bool:
        return bool(data.intersection(set(what)))

    @staticmethod
    def _any_not_in_list(what: Iterable[str], data: set[str]) -> bool:
        return bool(set(what).difference(data))


class In(ListRule):
    """
    Is item in list?
    For example:
        Policy: actions={'method': In(data={'read', 'write', 'delete'})}
        Example in Inquiry: action={'method': 'read'}
    """

    rule_type: Literal["In"] = "In"

    def satisfied(self, what: str, inquiry: None = None) -> bool:
        return self._one_in_list(what, self.data)


class NotIn(ListRule):
    """
    Is not item in the list?
    For example:
        Policy: actions=[{'method': NotIn(data={'read', 'write', 'delete'}]
        Example in Inquiry: action={'method': 'purge'}
    """

    rule_type: Literal["NotIn"] = "NotIn"

    def satisfied(self, what: str, inquiry: None = None) -> bool:
        return not self._one_in_list(what, self.data)


class AllIn(ListRule):
    """
    Are all the items in the list?
    For example:
        Policy: actions=[{'methods': AllIn(data={'read', 'write', 'delete'})}].
        Example in Inquiry: action={'method': ['purge', 'get]}
    """

    rule_type: Literal["AllIn"] = "AllIn"

    def satisfied(self, what: list[str], inquiry: None = None) -> bool:
        if not isinstance(what, list):
            raise TypeError("Value should be of list type")

        return self._all_in_list(what, self.data)


class AllNotIn(ListRule):
    """
    Are all the items not in the list?
    For example:
        Policy: actions=[{'methods': AllNotIn(data={'read', 'write', 'delete'})}].
        Example in Inquiry: action={'method': ['list', 'get]}
    """

    rule_type: Literal["AllNotIn"] = "AllNotIn"

    def satisfied(self, what: list[str], inquiry: None = None) -> bool:
        if not isinstance(what, list):
            raise TypeError("Value should be of list type")

        return not self._all_in_list(what, self.data)


class AnyIn(ListRule):
    """
    Are any of the items in the list?
    For example:
        Policy: actions=[{'methods': AnyIn(data={'read', 'write', 'delete'})}].
        Example in Inquiry: action={'method': ['list', 'get]}
    """

    rule_type: Literal["AnyIn"] = "AnyIn"

    def satisfied(self, what: list[str], inquiry: None = None) -> bool:
        if not isinstance(what, list):
            raise TypeError("Value should be of list type")

        return self._any_in_list(what, self.data)


class AnyNotIn(ListRule):
    """
    Are any of the items not in the list?
    For example:
        Policy: actions=[{'methods': AnyNotIn(data={'read', 'write', 'delete'})}].
        Example in Inquiry: action={'method': ['list', 'get]}
    """

    rule_type: Literal["AnyNotIn"] = "AnyNotIn"

    def satisfied(self, what: list[str], inquiry: None = None) -> bool:
        if not isinstance(what, list):
            raise TypeError("Value should be of list type")

        return self._any_not_in_list(what, self.data)
