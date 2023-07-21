import pytest
from queries import job as job_query
from schemas import JobInSchema
from pydantic import ValidationError


@pytest.mark.asyncio
async def test_get_all_jobs(sa_session, setup_job):
    all_jobs = await job_query.get_all_jobs(sa_session)
    assert all_jobs
    assert len(all_jobs) == 1
    assert all_jobs[0] == setup_job


@pytest.mark.asyncio
async def test_get_job_by_id(sa_session, setup_job):
    current_job = await job_query.get_job_by_id(sa_session, setup_job.id)
    assert current_job
    assert current_job.id == setup_job.id


@pytest.mark.asyncio
async def test_create_job(sa_session, setup_user):
    job = JobInSchema(
        title="Button presser",
        description="Very simple job",
        salary_from=10000,
        salary_to=20000,
        is_active=True
    )

    new_job = await job_query.create_job(sa_session, job_schema=job, current_user=setup_user)
    assert new_job
    assert new_job.user_id == setup_user.id
    assert new_job.title == "Button presser"
    assert new_job.description == "Very simple job"
    assert new_job.salary_from == 10000
    assert new_job.salary_to == 20000
    assert new_job.is_active


@pytest.mark.asyncio
async def test_swap_salary(sa_session, setup_user):
    with pytest.raises(ValidationError):
        job = JobInSchema(
            title="Button presser",
            description="Very simple job",
            salary_from=20000,
            salary_to=10000,
            is_active=True
        )
        await job_query.create_job(sa_session, job_schema=job, current_user=setup_user)


@pytest.mark.asyncio
async def test_negative_salary_from(sa_session, setup_user):
    with pytest.raises(ValidationError):
        job = JobInSchema(
            title="Button presser",
            description="Very simple job",
            salary_from=-10000,
            salary_to=20000,
            is_active=True
        )
        await job_query.create_job(sa_session, job_schema=job, current_user=setup_user)


@pytest.mark.asyncio
async def test_negative_salary_to(sa_session, setup_user):
    with pytest.raises(ValidationError):
        job = JobInSchema(
            title="Button presser",
            description="Very simple job",
            salary_from=10000,
            salary_to=-20000,
            is_active=True
        )
        await job_query.create_job(sa_session, job_schema=job, current_user=setup_user)


@pytest.mark.asyncio
async def test_delete_job(sa_session, setup_job):
    deleted_job = await job_query.delete_job(sa_session, setup_job.id)
    assert deleted_job
    assert not await job_query.get_job_by_id(sa_session, setup_job.id)
