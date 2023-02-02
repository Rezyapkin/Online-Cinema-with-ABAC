"""
Namespace for a basic Policy class.
"""
from uuid import UUID

from pydantic import Field

from .effects import Effects
from .utils import BaseOrjsonModel, PrettyPrint
from .rules import RuleType


class Policy(BaseOrjsonModel, PrettyPrint):
    """Represents a policy that regulates access and allowed actions of subjects
    over some resources under a set of context restrictions.
    """

    id: UUID | None
    effect: Effects = Field(default=Effects.DENY_ACCESS)
    subjects: list[RuleType | dict[str, RuleType]] = Field(default_factory=tuple)
    resources: list[RuleType | dict[str, RuleType]] = Field(default_factory=tuple)
    actions: list[RuleType | dict[str, RuleType]] = Field(default_factory=tuple)
    context: dict[str, RuleType] = Field(default_factory=dict)
    description: str

    def allow_access(self) -> bool:
        """Does policy imply allow-access?"""
        return self.effect == Effects.ALLOW_ACCESS


class PolicyAllow(Policy):
    """
    Policy that has effect ALLOW_ACCESS by default.
    """

    effect: Effects = Field(default=Effects.ALLOW_ACCESS)


class PolicyDeny(Policy):
    """
    Policy that has effect DENY_ACCESS by default.
    """

    effect: Effects = Field(default=Effects.DENY_ACCESS)
