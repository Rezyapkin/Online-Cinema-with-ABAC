"""
Audit logging for ABAC decisions.
"""
from typing import Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from .policy import Policy


class BasePoliciesMsg:
    def __init__(self, policies: Iterable | None = None):
        if not policies:
            policies = ()

        self.policies: Iterable["Policy"] = policies


class PoliciesNopMsg(BasePoliciesMsg):
    """
    Class for converting Policies collection into a string during logging.
    Returns an empty string message for the polices collection.
    """

    def __str__(self):
        return ""


class PoliciesDescriptionMsg(BasePoliciesMsg):
    """
    Class for converting Policies collection into a string during logging.
    Returns Policies description message for the polices collection.
    Example message: ['Policy 1 for Admins', 'Policy for regular users']
    """

    def __str__(self):
        line_breaker = "\n"
        descriptions = [
            f"id: {policy.id}, description: {' '.join(policy.description.replace(line_breaker, ' ').split())}"
            for policy in self.policies
        ]
        return f"[{', '.join(descriptions)}]"
