from decimal import Decimal
import datetime
from typing import Optional
from pydantic import BaseModel, validator


class JobSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str
    description: Optional[str] = None
    salary_from: Decimal
    salary_to: Decimal
    is_active: bool = True
    created_at: datetime.datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 123,
                "user_id": 123,
                "title": "Sofa tester",
                "description": "Required a professional sofa tester",
                 "salary_from": 42500.25,
                "salary_to": 52500.25,
                "is_active": True,
            }
        }

        orm_mode = True


class JobInSchema(BaseModel):
    title: str
    description: Optional[str] = None
    salary_from: Decimal
    salary_to: Decimal
    is_active: bool = True

    class Config:
        schema_extra = {
            "example": [
                {
                    "title": "Sofa tester",
                    "description": "Required a professional sofa tester",
                    "salary_from": 42500.25,
                    "salary_to": 52500.25,
                    "is_active": True,
                }
            ]
        }

    @validator("salary_from")
    def salary_from_correctness(cls, v, values, **kwargs):
        if v < 0:
            raise ValueError("Отрицательная зарплата")
        return v

    @validator("salary_to")
    def salary_to_correctness(cls, v, values, **kwargs):
        if 'salary_from' in values and v < values["salary_from"]:
            raise ValueError("Верхняя планка зарплаты меньше нижней")
        if v < 0:
            raise ValueError("Отрицательная зарплата")
        return v
