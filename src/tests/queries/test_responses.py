import pytest
from queries import response as response_query
from fixtures.jobs import JobFactory
from fixtures.users import UserFactory
from fixtures.responses import ResponseFactory
from schemas import ResponseInSchema


@pytest.mark.asyncio
async def test_get_responses_by_job_id(sa_session):
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

    responses = await response_query.get_responses_by_job_id(sa_session, job_id=job.id)
    assert responses
    assert len(responses) == 1
    assert responses[0] == response


@pytest.mark.asyncio
async def test_response_job(sa_session):
    company = UserFactory.build()
    company.is_company = True
    sa_session.add(company)
    job = JobFactory.build()
    job.user_id = company.id
    sa_session.add(job)
    user = UserFactory.build()
    user.is_company = False
    sa_session.add(user)
    sa_session.flush()

    response = ResponseInSchema(
        job_id=job.id,
        message="I want to work here"
    )

    new_response = await response_query.response_job(sa_session, response_schema=response, current_user=user)
    assert new_response is not None
    assert new_response.job_id == job.id
    assert new_response.user_id == user.id
    assert new_response.message == "I want to work here"


@pytest.mark.asyncio
async def test_get_response_by_id(sa_session):
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

    current_response = await response_query.get_response_by_id(sa_session, response_id=response.id)
    assert current_response is not None
    assert current_response.id == response.id
