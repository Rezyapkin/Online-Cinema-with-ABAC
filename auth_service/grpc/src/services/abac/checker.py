"""
Module for various checkers.
"""

from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .guard import Inquiry
    from .policy import Policy
    from .rules import RuleType

from loguru import logger


class Checker(ABC):
    """
    Abstract class for Checker typing.
    """

    @abstractmethod
    def fits(self, policy: "Policy", field: str, what: Any, inquiry: Union["Inquiry", None] = None):
        """
        Check if fields from Inquiry fit some Policies
        """
        pass


class RulesChecker(Checker):
    """
    Checker that uses Rules defined inside dictionaries to determine match.
    """

    def fits(self, policy: "Policy", field: str, what: Any, inquiry: Union["Inquiry", None] = None):
        """Does Policy fit the given 'what' value by its 'field' property"""
        where_list = getattr(policy, field, [])
        is_what_dict = isinstance(what, dict)

        for i in where_list:
            item_result = False
            # If not dict or Rule, skip it - we are not meant to handle it.
            # Do not use isinstance for higher execution speed
            if type(i) == dict:
                for key, rule in i.items():
                    if not is_what_dict:
                        logger.debug("Error matching Policy: data {} in Inquiry is not `dict`", what)
                        item_result = False
                    # at least one missing key in inquiry's data means no match for this item
                    elif key not in what:
                        logger.debug('Error matching Policy: data {} has no key "{}" required by Policy', what, key)
                        item_result = False
                    else:
                        what_value = what[key]
                        item_result = self._check_satisfied(rule, what_value, inquiry)
                    # at least one item's key didn't satisfy -> fail fast: policy doesn't fit anyway
                    if not item_result:
                        break
            elif callable(getattr(i, "satisfied", "")):
                item_result = self._check_satisfied(i, what, inquiry)
            # If at least one item fits -> policy fits for this field
            if item_result:
                return True

        return False

    @staticmethod
    def _check_satisfied(rule: "RuleType", what_value: Any, inquiry: Union["Inquiry", None] = None):
        try:
            return rule.satisfied(what_value, inquiry)
        except Exception:
            logger.exception("Error matching Policy, because of raised exception")
            return False
