"""
All Rules that work with strings.
"""

import re
from abc import ABC
from typing import Pattern, Literal


from pydantic import validator
from loguru import logger


from ..rules.base import Rule


class StringRule(Rule, ABC):
    """
    Basic Rule for strings
    """

    value: str
    case_sensitive: bool


class StrEqual(StringRule):
    """
    Rule that is satisfied if the string value equals the specified property of this rule.
    Performs case-sensitive and case-sensitive comparisons (based on `ci` (case_insensitive) flag).
    For example:
        Policy: context={'country': Equal(value='Mozambique', case_sensitive=True)}
        Example in Inquiry: context={'country': mozambique}
    """

    rule_type: Literal["StrEqual"] = "StrEqual"

    def satisfied(self, what: str, inquiry: None = None) -> bool:
        if isinstance(what, str):
            if self.case_sensitive:
                return what.lower() == self.value.lower()
            return what == self.value
        return False


class StrStartsWith(StringRule):
    """
    Rule that is satisfied when given string starts with initially provided substring.
    For example:
        Policy: context={'file': StartsWith(value='Route-', case_sensitive=True)}
        Example in Inquiry: context={'file': 'route-12.txt}
    """

    rule_type: Literal["StrStartsWith"] = "StrStartsWith"

    def satisfied(self, what: str, inquiry: None = None) -> bool:
        if isinstance(what, str):
            if self.case_sensitive:
                return what.lower().startswith(self.value.lower())
            return what.startswith(self.value)
        return False


class StrEndsWith(StringRule):
    """
    Rule that is satisfied when given string ends with initially provided substring.
    For example:
        Policy: context={'file': EndsWith(value='.txt', case_sensitive=True)}
        Example in Inquiry: context={'file': 'route-12.TXT}
    """

    rule_type: Literal["StrEndsWith"] = "StrEndsWith"

    def satisfied(self, what, inquiry: None = None) -> bool:
        if isinstance(what, str):
            if self.case_sensitive:
                return what.lower().endswith(self.value.lower())
            return what.endswith(self.value)
        return False


class StrContains(StringRule):
    """
    Rule that is satisfied when given string contains initially provided substring.
    For example:
        Policy: context={'file': Contains(value='SUN', case_sensitiveTrue)}
        Example in Inquiry: context={'file': 'sUnny_day.txt}
    """

    rule_type: Literal["StrContains"] = "StrContains"

    def satisfied(self, what, inquiry: None = None) -> bool:
        if isinstance(what, str):
            if self.case_sensitive:
                return self.value.lower() in what.lower()
            return self.value in what
        return False


class StrPairsEqual(Rule):
    """
    Rule that is satisfied when given data is an array of pairs and
    those pairs are represented by equal to each other strings.

    For example:
        Policy: context={'scores': PairsEqual()}
        Example in Inquiry: context={'scores': [1, 1]}
    """

    rule_type: Literal["StrPairsEqual"] = "StrPairsEqual"

    def satisfied(self, what: list[str], inquiry: None = None) -> bool:
        if not isinstance(what, list):
            return False

        for pair in what:
            if len(pair) != 2:
                return False

            if not isinstance(pair[0], str) and not isinstance(pair[1], str):
                return False

            if pair[0] != pair[1]:
                return False

        return True


class RegexMatch(Rule):
    r"""
    Rule that is satisfied when given data matches the provided regular expression.
    Note, that you should provide syntactically valid regular-expression string.
    For example:
        Policy: context={'file': RegexMatch(regex=r'\.(rb|sh|py|exe)$')}
        Example in Inquiry: context={'file': 'test.rb')}
    """
    rule_type: Literal["RegexMatch"] = "RegexMatch"
    regex: str | Pattern

    @validator("regex")
    def validate_regex(cls, v):  # noqa: N805
        try:
            v: Pattern = re.compile(v)
        except Exception as e:
            logger.exception("{} creation. Failed to compile regexp {}", type(cls).__name__, v)
            raise TypeError("pattern should be a valid regexp string. Error %s" % e)

        return v

    def satisfied(self, what, inquiry: None = None) -> bool:
        return bool(self.regex.match(str(what)))
