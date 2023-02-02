"""
All Rules for defining Inquiry elements relations
"""
from abc import ABC, abstractmethod

from typing import Any, Literal

from ..guard import Inquiry
from ..rules.base import Rule


class InquiryMatchAbstract(Rule, ABC):
    """
    Base rule for concrete InquiryMatch rule implementations.
    """

    attribute: str | None

    def satisfied(self, what: Any, inquiry: Inquiry | None = None) -> bool:
        if not inquiry:
            return False

        inquiry_value = getattr(inquiry, self._field_name())

        if self.attribute is not None:
            if isinstance(inquiry_value, dict) and self.attribute in inquiry_value:
                inquiry_value = inquiry_value[self.attribute]
            else:
                return False

        return what == inquiry_value

    @abstractmethod
    def _field_name(self) -> str:
        pass


class SubjectMatch(InquiryMatchAbstract):
    """
    Rule that is satisfied if the value equals the Inquiry's Subject or it's attribute.
    For example:
        Policy: resources=[{'id': SubjectMatch()}]
        Example in Inquiry: Inquiry(subject='Max', resource={'id': 'Max'})
    """

    rule_type: Literal["SubjectMatch"] = "SubjectMatch"

    def _field_name(self) -> str:
        return "subject"


class ActionMatch(InquiryMatchAbstract):
    """
    Rule that is satisfied if the value equals the Inquiry's Action or it's attribute.
    For example:
        Policy:  subjects=[ActionMatch('id')]
        Example in Inquiry: Inquiry(subject='Max', action={'method': 'get', id': 'Max'})
    """

    rule_type: Literal["ActionMatch"] = "ActionMatch"

    def _field_name(self) -> str:
        return "action"


class ResourceMatch(InquiryMatchAbstract):
    """
    Rule that is satisfied if the value equals the Inquiry's Resource or it's attribute.
    For example:
        Policy: subjects=[ResourceMatch('id')]
        Example in Inquiry: Inquiry(subject='Max', resource={'res': 'book', id': 'Max'})
    """

    rule_type: Literal["ResourceMatch"] = "ResourceMatch"

    def _field_name(self) -> str:
        return "resource"
