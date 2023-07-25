from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ResponseSchema, ResponseInSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import response as response_queries
from queries import job as job_queries
from models import User


router = APIRouter(prefix="/responses", tags=["responses"])


@router.post("", response_model=ResponseSchema)
async def response_job(
        response: ResponseInSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    if not current_user or current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав для отклика на вакансию")

    job = await job_queries.get_job_by_id(db=db, job_id=response.job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена")

    job = await response_queries.create_response(db=db, response_schema=response, current_user=current_user)
    return ResponseSchema.from_orm(job)


@router.get("", response_model=List[ResponseSchema])
async def read_responses_by_job_id(
        job_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
        limit: int = 100,
        skip: int = 0):
    job = await job_queries.get_job_by_id(db=db, job_id=job_id)
    if not current_user or not current_user.is_company or job.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав для чтения вакансий")

    return await response_queries.get_responses_by_job_id(db=db, job_id=job_id, limit=limit, skip=skip)


@router.delete("", response_model=ResponseSchema)
async def delete_response(
        response_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    response = await response_queries.get_response_by_id(db=db, response_id=response_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отклик не найден")
    if current_user.id != response.user_id or current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав для удаления вакансии")

    response = await response_queries.delete_response(db=db, response_id=response.id)

    return ResponseSchema.from_orm(response)
