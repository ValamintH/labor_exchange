from models import Response, User
from schemas import ResponseInSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional


async def response_job(db: AsyncSession, response_schema: ResponseInSchema, current_user: User) -> Response:
    response = Response(
        job_id=response_schema.job_id,
        user_id=current_user.id,
        message=response_schema.message,
    )
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response


async def get_responses_by_job_id(db: AsyncSession, job_id: int, limit: int = 100, skip: int = 0) -> List[Response]:
    query = select(Response).where(Response.job_id == job_id).limit(limit).offset(skip)
    res = await db.execute(query)
    return res.scalars().all()


async def get_response_by_id(db: AsyncSession, response_id: int) -> Optional[Response]:
    query = select(Response).where(Response.id == response_id).limit(1)
    res = await db.execute(query)
    return res.scalars().first()


async def delete_response(db: AsyncSession, response: Response) -> Response:
    await db.delete(response)
    await db.commit()
    return response


