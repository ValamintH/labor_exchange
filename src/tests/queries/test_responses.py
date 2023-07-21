import pytest
from queries import response as response_query
from fixtures.users import UserFactory
from fixtures.responses import ResponseFactory
from schemas import ResponseInSchema


@pytest.mark.asyncio
async def test_get_responses_by_job_id(sa_session, setup_job):
    user = UserFactory.build()
    user.is_company = False
    sa_session.add(user)
    response = ResponseFactory.build()
    response.job_id = setup_job.id
    response.user_id = user.id
    sa_session.add(response)
    sa_session.flush()

    responses = await response_query.get_responses_by_job_id(sa_session, job_id=setup_job.id)
    assert responses
    assert len(responses) == 1
    assert responses[0] == response


@pytest.mark.asyncio
async def test_response_job(sa_session, setup_job):
    user = UserFactory.build()
    user.is_company = False
    sa_session.add(user)
    sa_session.flush()

    response = ResponseInSchema(
        job_id=setup_job.id,
        message="I want to work here"
    )

    new_response = await response_query.create_response(sa_session, response_schema=response, current_user=user)
    assert new_response
    assert new_response.job_id == setup_job.id
    assert new_response.user_id == user.id
    assert new_response.message == "I want to work here"


@pytest.mark.asyncio
async def test_get_response_by_id(sa_session, setup_response):
    current_response = await response_query.get_response_by_id(sa_session, response_id=setup_response.id)
    assert current_response
    assert current_response.id == setup_response.id


@pytest.mark.asyncio
async def test_delete_response(sa_session, setup_response):
    deleted_response = await response_query.delete_response(sa_session, setup_response.id)
    assert deleted_response
    assert not await response_query.get_response_by_id(sa_session, setup_response.id)
