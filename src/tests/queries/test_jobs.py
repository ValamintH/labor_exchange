import pytest
from queries import job as job_query
from fixtures.jobs import JobFactory
from fixtures.users import UserFactory
from schemas import JobInSchema
from pydantic import ValidationError


@pytest.mark.asyncio
async def test_get_all_jobs(sa_session):
    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)
    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    sa_session.flush()

    all_jobs = await job_query.get_all_jobs(sa_session)
    assert all_jobs
    assert len(all_jobs) == 1
    assert all_jobs[0] == job


@pytest.mark.asyncio
async def test_get_job_by_id(sa_session):
    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)
    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    sa_session.flush()

    current_job = await job_query.get_job_by_id(sa_session, job.id)
    assert current_job is not None
    assert current_job.id == job.id


@pytest.mark.asyncio
async def test_create_job(sa_session):
    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)
    sa_session.flush()

    job = JobInSchema(
        title="Button presser",
        description="Very simple job",
        salary_from=10000,
        salary_to=20000,
        is_active=True
    )

    new_job = await job_query.create_job(sa_session, job_schema=job, current_user=user)
    assert new_job is not None
    assert new_job.user_id == user.id
    assert new_job.title == "Button presser"
    assert new_job.description == "Very simple job"
    assert new_job.salary_from == 10000
    assert new_job.salary_to == 20000
    assert new_job.is_active


@pytest.mark.asyncio
async def test_swap_salary(sa_session):
    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)
    sa_session.flush()
    with pytest.raises(ValidationError):
        job = JobInSchema(
            title="Button presser",
            description="Very simple job",
            salary_from=20000,
            salary_to=10000,
            is_active=True
        )
        await job_query.create_job(sa_session, job_schema=job, current_user=user)


@pytest.mark.asyncio
async def test_negative_salary_from(sa_session):
    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)
    sa_session.flush()
    with pytest.raises(ValidationError):
        job = JobInSchema(
            title="Button presser",
            description="Very simple job",
            salary_from=-10000,
            salary_to=20000,
            is_active=True
        )
        await job_query.create_job(sa_session, job_schema=job, current_user=user)


@pytest.mark.asyncio
async def test_negative_salary_to(sa_session):
    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)
    sa_session.flush()
    with pytest.raises(ValidationError):
        job = JobInSchema(
            title="Button presser",
            description="Very simple job",
            salary_from=10000,
            salary_to=-20000,
            is_active=True
        )
        await job_query.create_job(sa_session, job_schema=job, current_user=user)


@pytest.mark.asyncio
async def test_delete_job(sa_session):
    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)
    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    sa_session.flush()

    deleted_job = await job_query.delete_job(sa_session, job)
    assert deleted_job is not None
    assert deleted_job.id == job.id
