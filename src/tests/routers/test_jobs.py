import pytest
from schemas import JobInSchema
from fastapi import status
import json


@pytest.mark.asyncio
async def test_read_jobs(client_app, setup_job):
    response = await client_app.get(url="/jobs")
    assert response
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == setup_job.title


@pytest.mark.asyncio
async def test_read_job_by_id(client_app, setup_job):
    response = await client_app.get(url=f"/jobs/{setup_job.id}")
    assert response
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == setup_job.title


@pytest.mark.asyncio
async def test_read_job_by_bad_id(client_app):
    response = await client_app.get(url="/jobs/999")
    assert response
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_job(client_app, sa_session, current_user):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    job = JobInSchema(
        title="Best work",
        description="Do nothing",
        salary_from=200.22,
        salary_to=400.33,
        is_active=False
    )
    r = json.loads(job.json())
    response = await client_app.post(url="/jobs", json=r)
    assert response
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Best work"
    assert response.json()["description"] == "Do nothing"
    assert response.json()["salary_from"] == 200.22
    assert response.json()["salary_to"] == 400.33
    assert not response.json()["is_active"]


@pytest.mark.asyncio
async def test_delete_job(client_app, sa_session, current_user, setup_job):
    current_user.is_company = True
    sa_session.add(current_user)
    setup_job.user_id = current_user.id
    sa_session.add(setup_job)
    sa_session.flush()

    response = await client_app.delete(url=f"/jobs?job_id={setup_job.id}")
    assert response
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == setup_job.id


@pytest.mark.asyncio
async def test_delete_bad_id_job(client_app, sa_session, current_user):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    response = await client_app.delete(url="/jobs?job_id=999")
    assert response
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_job_wrong_ids(client_app, sa_session, current_user, setup_job):
    current_user.is_company = True
    sa_session.add(current_user)
    setup_job.user_id = current_user.id + 1
    sa_session.add(setup_job)
    sa_session.flush()

    response = await client_app.delete(url=f"/jobs?job_id={setup_job.id}")
    assert response
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_delete_job_not_company(client_app, sa_session, current_user, setup_job):
    current_user.is_company = False
    sa_session.add(current_user)
    setup_job.user_id = current_user.id
    sa_session.add(setup_job)
    sa_session.flush()

    response = await client_app.delete(url=f"/jobs?job_id={setup_job.id}")
    assert response
    assert response.status_code == status.HTTP_403_FORBIDDEN
