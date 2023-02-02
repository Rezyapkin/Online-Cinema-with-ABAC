import asyncio
from contextlib import asynccontextmanager
from functools import wraps
from typing import AsyncGenerator

import click
from grpc_auth_service.utils import Constants, Services
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import get_settings
from db.storage.postgres.abac import ABACCrudStorage
from db.storage.postgres.user import UserCrudStorage
from models.postgres.abac import PolicyModelSchema
from models.postgres.user import UserSchema
from services.abac.policy import PolicyAllow, PolicyDeny
from services.abac.rules import StrStartsWith, StrEqual, RuleAny, Falsy


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@asynccontextmanager
async def get_session(session_maker: sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    """Relational SQL storage Provider."""
    try:
        db = session_maker()
        yield db
    finally:
        await db.close()


@click.group()
def cli():
    pass


@cli.command()
@coro
@click.option("--email", help="User email")
@click.option("--password", help="User password")
async def createsuperuser(email, password):
    engine = create_async_engine(get_settings().postgres_dsn, echo=True, future=True)
    session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with get_session(session_maker=session_maker) as session:
        user_manager = UserCrudStorage(client=session)

        try:
            await user_manager.create(obj_in=UserSchema(email=email, hashed_password=password, is_superuser=True))
        except IntegrityError:
            pass

        click.echo("Success!")


@cli.command()
@coro
async def create_default_policy():
    engine = create_async_engine(get_settings().postgres_dsn, echo=True, future=True)
    session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with get_session(session_maker=session_maker) as session:
        abac_pip_manager = ABACCrudStorage(client=session)

        try:
            policy = PolicyAllow(
                actions=[StrEqual(value=Constants.ACTION_GET, case_sensitive=False)],
                resources=[
                    {
                        Constants.RESOURCE_PATH: StrStartsWith(value="/api/v1", case_sensitive=False),
                        Constants.RESOURCE_SERVICE: RuleAny(),
                    }
                ],
                subjects=[{Constants.SUBJECT_IS_USER: RuleAny(), Constants.SUBJECT_IS_SUPERUSER: RuleAny()}],
                context={Constants.CONTEXT_IP_ADDRESS: RuleAny(), Constants.CONTEXT_USER_AGENT: RuleAny()},
                description="""
                    Base rule to allow all GET api/v1/* calls.
                """,
            )
            await abac_pip_manager.create(obj_in=PolicyModelSchema(**policy.dict()))
        except IntegrityError:
            pass

        try:
            policy = PolicyDeny(
                actions=[StrEqual(value=Constants.ACTION_POST, case_sensitive=False)],
                resources=[
                    {
                        Constants.RESOURCE_PATH: StrStartsWith(value="/api/v1/films", case_sensitive=False),
                        Constants.RESOURCE_SERVICE: StrEqual(
                            value=Services.MOVIES_SEARCH_SERVICE, case_sensitive=False
                        ),
                    }
                ],
                subjects=[{Constants.SUBJECT_IS_USER: RuleAny(), Constants.SUBJECT_IS_SUPERUSER: Falsy()}],
                context={Constants.CONTEXT_IP_ADDRESS: RuleAny(), Constants.CONTEXT_USER_AGENT: RuleAny()},
                description="""
                    Disable POST films for everyone, except superuser.
                """,
            )
            await abac_pip_manager.create(obj_in=PolicyModelSchema(**policy.dict()))
        except IntegrityError:
            pass

        click.echo("Success!")


cli()
