""""
Main module that serves as an entry point for ABAC decisions.
Also contains Inquiry class.
"""
from pydantic import Field
from typing import AsyncGenerator, TYPE_CHECKING

from core.tracer import instrumented

if TYPE_CHECKING:
    from db.storage.postgres.abac import ABACCrudStorage
    from .policy import Policy

from loguru import logger

from .checker import Checker, RulesChecker
from .utils import BaseOrjsonModel, PrettyPrint
from .audit import PoliciesDescriptionMsg, BasePoliciesMsg
from .effects import Effects


class Inquiry(BaseOrjsonModel, PrettyPrint):
    """Holds all the information about the inquired intent.
    Is responsible to decisions if the inquired intent allowed or not."""

    resource: str | dict = Field(default="")
    action: str | dict = Field(default="")
    subject: str | dict = Field(default="")
    context: str | dict = Field(default_factory=dict)


class Guard:
    """
    Executor of policy checks.
    Given a storage and a checker it can decide via `is_allowed` method if a given inquiry allowed or not.

    storage - what storage to use
    checker - what checker to use
    audit_policies_cls - what message class to use for logging Policies in audit
    """

    def __init__(
        self,
        storage: "ABACCrudStorage",
        checker: Checker | None = None,
        audit_policies_cls: type[BasePoliciesMsg] | None = None,
    ):
        if audit_policies_cls is None:
            audit_policies_cls = PoliciesDescriptionMsg

        if checker is None:
            checker = RulesChecker()

        self.storage: "ABACCrudStorage" = storage
        self.checker: Checker = checker
        self.apm: type[BasePoliciesMsg] = audit_policies_cls

    @instrumented
    async def is_allowed(self, inquiry: "Inquiry") -> bool:
        """
        Is given inquiry intent allowed or not?
        Same as `is_allowed_check`, but also logs policy enforcement decisions to log for every incoming inquiry.
        Is meant to be used by an end-user.
        """
        answer = await self._is_allowed_check(inquiry)

        if answer:
            logger.debug("Incoming Inquiry was allowed. Inquiry: {}", inquiry)
        else:
            logger.debug("Incoming Inquiry was rejected. Inquiry: {}", inquiry)

        return answer

    async def _is_allowed_check(self, inquiry: "Inquiry") -> bool:
        """
        Is given inquiry intent allowed or not?
        Is not meant to be called by an end-user. Use it only if you want the core functionality of allowance check.
        """
        answer = False

        try:
            policies: AsyncGenerator["Policy", None] = self.storage.find_for_inquiry()
            # Storage is not obliged to do the exact policies match. It's up to the storage
            # to decide what policies to return. So we need a more correct programmatically done check.
            answer = await self._check_policies_allow(inquiry, policies)
        except Exception:
            logger.exception("Unexpected exception occurred while checking Inquiry {}", inquiry)

        return answer

    async def _check_policies_allow(self, inquiry: "Inquiry", policies: AsyncGenerator["Policy", None]) -> bool:
        """
        Check if any of a given policy allows a specified inquiry
        """
        # Filter policies that fit Inquiry by its attributes.
        filtered = [
            p
            async for p in policies
            if self.checker.fits(policy=p, field="actions", what=inquiry.action, inquiry=inquiry)
            and self.checker.fits(policy=p, field="subjects", what=inquiry.subject, inquiry=inquiry)
            and self.checker.fits(policy=p, field="resources", what=inquiry.resource, inquiry=inquiry)
            and self.check_context_restriction(policy=p, inquiry=inquiry)
        ]

        # no policies -> deny access!
        if len(filtered) == 0:
            logger.info(
                "No potential policies were found. Effect: {} for inquiry: {} with candidates: {} and deciders: {}",
                Effects.DENY_ACCESS,
                inquiry,
                self.apm(filtered),
                self.apm([]),
            )
            return False

        # if we have 2 or more similar policies - all of them should have allow effect, otherwise -> deny access!
        for p in filtered:
            if not p.allow_access():
                logger.info(
                    "One of matching policies has deny effect. "
                    "Effect: {} for inquiry: {} with candidates: {} and deciders: {}",
                    Effects.DENY_ACCESS,
                    inquiry,
                    self.apm(filtered),
                    self.apm([p]),
                )
                return False

        logger.info(
            "All matching policies have allow effect. Effect: {} for inquiry: {} with candidates: {} and deciders: {}",
            Effects.ALLOW_ACCESS,
            inquiry,
            self.apm(filtered),
            self.apm(filtered),
        )

        return True

    @staticmethod
    def check_context_restriction(policy: "Policy", inquiry: "Inquiry") -> bool:
        """
        Check if context restriction in the policy is satisfied for a given inquiry's context.
        If at least one rule is not present in Inquiry's context -> deny access.
        If at least one rule provided in Inquiry's context is not satisfied -> deny access.
        """
        for key, rule in policy.context.items():
            try:
                ctx_value = inquiry.context[key]
            except KeyError:
                logger.debug("No key '{}' found in Inquiry context", key)
                return False

            if not rule.satisfied(ctx_value, inquiry):
                return False

        return True
