import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from main import app
import pytest
import pytest_asyncio
from unittest.mock import MagicMock
from db_settings import SQLALCHEMY_DATABASE_URL
from sqlalchemy import inspect
from models import User, Job, Response
from schemas import TokenSchema
from core.security import create_access_token
from httpx import AsyncClient
from dependencies import get_db


@pytest_asyncio.fixture()
async def client_app(sa_session: AsyncSession, access_token: TokenSchema):
    app.dependency_overrides[get_db] = lambda: sa_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        client.headers["Authorization"] = f"Bearer {access_token.access_token}"
        yield client


@pytest_asyncio.fixture()
async def sa_session():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)  # You must provide your database URL.
    connection = await engine.connect()
    trans = await connection.begin()

    Session = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)
    session = Session()

    deletion = session.delete

    async def mock_delete(instance):
        insp = inspect(instance)
        if not insp.persistent:
            session.expunge(instance)
        else:
            await deletion(instance)

        return await asyncio.sleep(0)

    session.commit = MagicMock(side_effect=session.flush)
    session.delete = MagicMock(side_effect=mock_delete)

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()
        await engine.dispose()


@pytest_asyncio.fixture()
async def current_user(sa_session: AsyncSession):
    new_user = UserFactory.build()
    sa_session.add(new_user)

    await sa_session.commit()
    await sa_session.refresh(new_user)

    return new_user


@pytest_asyncio.fixture()
async def access_token(current_user):
    token = TokenSchema(
        access_token=create_access_token({"sub": current_user.email}),
        token_type="Bearer"
    )
    return token


@pytest.fixture()
def setup_user(sa_session: AsyncSession) -> User:
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()
    return user


@pytest.fixture()
def setup_job(sa_session: AsyncSession) -> Job:
    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)
    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    sa_session.flush()
    return job


@pytest.fixture()
def setup_response(sa_session: AsyncSession) -> Response:
    company = UserFactory.build()
    company.is_company = True
    sa_session.add(company)
    job = JobFactory.build()
    job.user_id = company.id
    sa_session.add(job)
    user = UserFactory.build()
    user.is_company = False
    sa_session.add(user)
    response = ResponseFactory.build()
    response.job_id = job.id
    response.user_id = user.id
    sa_session.add(response)
    sa_session.flush()
    return response


# регистрация фабрик
@pytest_asyncio.fixture(autouse=True)
def setup_factories(sa_session: AsyncSession) -> None:
    UserFactory.session = sa_session
    JobFactory.session = sa_session
    ResponseFactory.session = sa_session
