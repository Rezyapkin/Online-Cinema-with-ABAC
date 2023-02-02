"""
All Rules that are related to logic and composition.
"""

from abc import ABC, abstractmethod
from typing import Callable, Any, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from . import RuleType

from ..guard import Inquiry
from ..rules.base import Rule


class BooleanRule(Rule, ABC):
    """
    Boolean Rule that is satisfied when 'what' is evaluated to a boolean true/false.
    Its `satisfied` accepts:
     - a callable without arguments
     - non-callable
     - expressions
    """

    def satisfied(self, what: Callable[[Any], Any] | Any, inquiry: None = None) -> bool:
        res = what() if callable(what) else what
        return bool(res) == self.val

    @property
    @abstractmethod
    def val(self) -> bool:
        """This should be overridden as a True/False getter property"""
        pass


class Truthy(BooleanRule):
    """
    Rule that is satisfied when 'what' is evaluated to a boolean 'true'.
    For example:
        Policy:  subjects=[{'role': Truthy(), 'name': Eq('Jimmy')}]
        Example in Inquiry: subjects={'role': user.is_admin()}
    """

    rule_type: Literal["Truthy"] = "Truthy"

    @property
    def val(self) -> bool:
        return True


class Falsy(BooleanRule):
    """
    Rule that is satisfied when 'what' is evaluated to a boolean 'false'.
    For example:
        Policy:  subjects=[{'role': Truthy(), 'name': Eq('Jimmy')}]
        Example in Inquiry: subjects={'role': not user.is_admin()}
    """

    rule_type: Literal["Falsy"] = "Falsy"

    @property
    def val(self) -> bool:
        return False


class CompositionRule(Rule, ABC):
    """
    Abstract Rule that encompasses other Rules.
    """

    rules: list["RuleType"]


class And(CompositionRule):
    """
    Rule that is satisfied when all the rules it's composed of are satisfied.
    For example:
        Policy: subjects=[{'stars': And(rules=(Greater(50), Less(120))), 'name': Eq('Jimmy')}]
        Example in Inquiry: subjects={'stars': 61}
    """

    rule_type: Literal["And"] = "And"

    def satisfied(self, what: Any, inquiry: Inquiry | None = None) -> bool:
        answers = [x.satisfied(what, inquiry) for x in self.rules]
        return len(answers) > 0 and all(answers)


class Or(CompositionRule):
    """
    Rule that is satisfied when at least one of the rules it's composed of is satisfied.
    Uses short-circuit evaluation.
    For example:
        Policy: subjects=[{'stars': Or(rules=(Less(50), Greater(120))), 'name': Eq('Jimmy')}]
        Example in Inquiry: subjects={'stars': 121}
    """

    rule_type: Literal["Or"] = "Or"

    def satisfied(self, what: Any, inquiry: Inquiry | None = None) -> bool:
        for rule in self.rules:
            if rule.satisfied(what, inquiry):
                return True

        return False


class Not(Rule):
    """
    Rule that negates another Rule.
    For example:
        Policy: subjects=[{'stars': Eq(555), 'name': Not(rule=Eq('Jimmy'))}]
        Example in Inquiry: subjects={'Not': "Jimmy 3221"}
    """

    rule_type: Literal["Not"] = "Not"
    rule: "RuleType"

    def satisfied(self, what: Any, inquiry: Inquiry | None = None) -> bool:
        return not self.rule.satisfied(what, inquiry)


class RuleAny(Rule):
    """
    Rule that is always satisfied.
    For example:
        Policy: resources=[{'endpoint': Any(), 'method': Eq('POST')}]
        Example in Inquiry: resources={'endpoint': "any_value"}

        Policy: actions=[Any()]
        ...: action='get', action='foo'
    """

    rule_type: Literal["RuleAny"] = "RuleAny"

    def satisfied(self, what: None = None, inquiry: None = None) -> bool:
        return True


class Neither(Rule):
    """
    Rule that always isn't satisfied.
    For example:
        Policy: resources=[{'endpoint': Any(), 'method': Eq('POST')}]
        Example in Inquiry: resources={'endpoint': "any_value"}

        Policy: subjects=[Neither()]
        ...: subject='Max', subject='Joe'
    """

    rule_type: Literal["Neither"] = "Neither"

    def satisfied(self, what: None = None, inquiry: None = None) -> bool:
        return False
