from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import JobSchema, JobInSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import job as job_queries
from models import User

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobSchema)
async def create_job(
        job: JobInSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    if current_user is None or not current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав для создания вакансии")
    job = await job_queries.create_job(db=db, job_schema=job, current_user=current_user)
    return JobSchema.from_orm(job)


@router.get("", response_model=List[JobSchema])
async def read_jobs(
        db: AsyncSession = Depends(get_db),
        limit: int = 100,
        skip: int = 0):
    return await job_queries.get_all_jobs(db=db, limit=limit, skip=skip)


@router.get("/{job_id}", response_model=JobSchema)
async def read_job_by_id(
        job_id: int,
        db: AsyncSession = Depends(get_db)):
    job = await job_queries.get_job_by_id(db=db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена")
    return JobSchema.from_orm(job)


@router.delete("", response_model=JobSchema)
async def delete_job(
        job_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    job = await job_queries.get_job_by_id(db=db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена")
    if current_user.id != job.user_id or not current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав для удаления вакансии")

    job = await job_queries.delete_job(db=db, job=job)

    return JobSchema.from_orm(job)
