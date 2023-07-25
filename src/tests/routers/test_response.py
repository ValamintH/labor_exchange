import pytest
from schemas import ResponseInSchema
from fastapi import status


@pytest.mark.asyncio
async def test_response_job(client_app, sa_session, current_user, setup_job):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    response_schema = ResponseInSchema(
        job_id=setup_job.id,
        message="Can do anything"
    )
    response = await client_app.post(url="/responses", json=response_schema.dict())
    assert response
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["job_id"] == setup_job.id
    assert response.json()["user_id"] == current_user.id
    assert response.json()["message"] == "Can do anything"


@pytest.mark.asyncio
async def test_response_job_is_company(client_app, sa_session, current_user, setup_job):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    response_schema = ResponseInSchema(
        job_id=setup_job.id,
        message="Can do anything"
    )
    response = await client_app.post(url="/responses", json=response_schema.dict())
    assert response
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_response_bad_id_job(client_app, sa_session, current_user):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    response_schema = ResponseInSchema(
        job_id=999,
        message="Can do anything"
    )
    response = await client_app.post(url="/responses", json=response_schema.dict())
    assert response
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_read_responses_by_id(client_app, sa_session, current_user, setup_job, setup_response):
    current_user.is_company = True
    sa_session.add(current_user)
    setup_job.user_id = current_user.id
    sa_session.add(setup_job)
    setup_response.job_id = setup_job.id
    sa_session.add(setup_response)
    sa_session.flush()

    response = await client_app.get(url=f"/responses?job_id={setup_response.job_id}")
    assert response
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["job_id"] == setup_response.job_id


@pytest.mark.asyncio
async def test_read_responses_by_id_not_company(client_app, sa_session, current_user, setup_job, setup_response):
    current_user.is_company = False
    sa_session.add(current_user)
    setup_job.user_id = current_user.id
    sa_session.add(setup_job)
    setup_response.job_id = setup_job.id
    sa_session.add(setup_response)
    sa_session.flush()

    response = await client_app.get(url=f"/responses?job_id={setup_response.job_id}")
    assert response
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_read_responses_by_id_wrong_ids(client_app, sa_session, current_user, setup_job, setup_response):
    current_user.is_company = True
    sa_session.add(current_user)
    setup_job.user_id = current_user.id + 1
    sa_session.add(setup_job)
    setup_response.job_id = setup_job.id
    sa_session.add(setup_response)
    sa_session.flush()

    response = await client_app.get(url=f"/responses?job_id={setup_response.job_id}")
    assert response
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_read_delete_response(client_app, sa_session, current_user, setup_response):
    current_user.is_company = False
    sa_session.add(current_user)
    setup_response.user_id = current_user.id
    sa_session.add(setup_response)
    sa_session.flush()

    response = await client_app.delete(url=f"/responses?response_id={setup_response.id}")
    assert response
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == setup_response.id


@pytest.mark.asyncio
async def test_read_delete_bad_id_response(client_app, sa_session, current_user):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    response = await client_app.delete(url="/responses?response_id=999")
    assert response
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_read_delete_response_wrong_ids(client_app, sa_session, current_user, setup_response):
    current_user.is_company = False
    sa_session.add(current_user)
    setup_response.user_id = current_user.id + 1
    sa_session.add(setup_response)
    sa_session.flush()

    response = await client_app.delete(url=f"/responses?response_id={setup_response.id}")
    assert response
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_read_delete_response_is_company(client_app, sa_session, current_user, setup_response):
    current_user.is_company = True
    sa_session.add(current_user)
    setup_response.user_id = current_user.id
    sa_session.add(setup_response)
    sa_session.flush()

    response = await client_app.delete(url=f"/responses?response_id={setup_response.id}")
    assert response
    assert response.status_code == status.HTTP_403_FORBIDDEN
