from pydantic import Field
from typing_extensions import Annotated

from .base import Rule
from .inquiry import SubjectMatch, ActionMatch, ResourceMatch
from .list import (
    In,
    NotIn,
    AllIn,
    AllNotIn,
    AnyIn,
    AnyNotIn,
)
from .logic import (
    Truthy,
    Falsy,
    And,
    Or,
    Not,
    RuleAny,
    Neither,
)
from .net import CIDR
from .operator import (
    Eq,
    NotEq,
    Greater,
    Less,
    GreaterOrEqual,
    LessOrEqual,
)
from .string import (
    StrEqual,
    StrStartsWith,
    StrEndsWith,
    StrContains,
    StrPairsEqual,
    RegexMatch,
)

RuleType = Annotated[
    SubjectMatch
    | ActionMatch
    | ResourceMatch
    | In
    | NotIn
    | AllIn
    | AllNotIn
    | AnyIn
    | AnyNotIn
    | Truthy
    | Falsy
    | And
    | Or
    | Not
    | RuleAny
    | Neither
    | CIDR
    | Eq
    | NotEq
    | Greater
    | Less
    | GreaterOrEqual
    | LessOrEqual
    | StrEqual
    | StrStartsWith
    | StrEndsWith
    | StrContains
    | StrPairsEqual
    | RegexMatch,
    Field(discriminator="rule_type"),
]


And.update_forward_refs(RuleType=RuleType)
Or.update_forward_refs(RuleType=RuleType)
Not.update_forward_refs(RuleType=RuleType)
