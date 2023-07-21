import pytest
from schemas import UserInSchema, UserUpdateSchema
from fastapi import status


@pytest.mark.asyncio
async def test_read_users(client_app, setup_user):
    response = await client_app.get(url="/users")
    assert response
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json()[1]["name"] == setup_user.name


@pytest.mark.asyncio
async def test_create_user(client_app):
    user = UserInSchema(
        name="Uchpochmak",
        email="bashkort@example.com",
        password="bobrbobr",
        password2="bobrbobr",
        is_company=False
    )
    response = await client_app.post(url="/users", json=user.dict())
    assert response
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Uchpochmak"
    assert response.json()["email"] == "bashkort@example.com"
    assert response.json()["hashed_password"] != "bobrbobr"
    assert not response.json()["is_company"]


@pytest.mark.asyncio
async def test_update_user(client_app, sa_session, current_user):
    sa_session.add(current_user)
    sa_session.flush()

    new_user = UserUpdateSchema(
        name="John Smith",
        email="johnsmith@mail.com",
        is_company=False
    )
    response = await client_app.put(url=f"/users?id={current_user.id}", json=new_user.dict())
    assert response
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == current_user.id
    assert response.json()["name"] == "John Smith"
    assert response.json()["email"] == "johnsmith@mail.com"
    assert not response.json()["is_company"]


@pytest.mark.asyncio
async def test_delete_user(client_app, sa_session, current_user):
    sa_session.add(current_user)
    sa_session.flush()

    response = await client_app.delete(url="/users")
    assert response
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == current_user.id
