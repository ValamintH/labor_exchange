import pytest
from queries import user as user_query
from schemas import UserInSchema
from pydantic import ValidationError


@pytest.mark.asyncio
async def test_get_all(sa_session, setup_user):
    all_users = await user_query.get_all(sa_session)
    assert all_users
    assert len(all_users) == 1
    assert all_users[0] == setup_user


@pytest.mark.asyncio
async def test_get_by_id(sa_session, setup_user):
    current_user = await user_query.get_by_id(sa_session, setup_user.id)
    assert current_user
    assert current_user.id == setup_user.id


@pytest.mark.asyncio
async def test_get_by_email(sa_session, setup_user):
    current_user = await user_query.get_by_email(sa_session, setup_user.email)
    assert current_user
    assert current_user.id == setup_user.id


@pytest.mark.asyncio
async def test_create(sa_session):
    user = UserInSchema(
        name="Uchpochmak",
        email="bashkort@example.com",
        password="eshkere!",
        password2="eshkere!",
        is_company=False
    )

    new_user = await user_query.create(sa_session, user_schema=user)
    assert new_user
    assert new_user.name == "Uchpochmak"
    assert new_user.email == "bashkort@example.com"
    assert new_user.hashed_password != "eshkere!"
    assert not new_user.is_company


@pytest.mark.asyncio
async def test_create_password_mismatch(sa_session):
    with pytest.raises(ValidationError):
        user = UserInSchema(
            name="Uchpochmak",
            email="bashkort@example.com",
            password="eshkere!",
            password2="eshkero!",
            is_company=False
        )
        await user_query.create(sa_session, user_schema=user)


@pytest.mark.asyncio
async def test_update(sa_session, setup_user):
    setup_user.name = "updated_name"
    updated_user = await user_query.update(sa_session, user=setup_user)
    assert setup_user.id == updated_user.id
    assert updated_user.name == "updated_name"


@pytest.mark.asyncio
async def test_delete_user(sa_session, setup_user):
    deleted_user = await user_query.delete_user(sa_session, setup_user.id)
    assert deleted_user
    assert not await user_query.get_by_id(sa_session, setup_user.id)
