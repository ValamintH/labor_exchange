from typing import Optional
from pydantic import BaseModel


class ResponseSchema(BaseModel):
    id: Optional[int] = None
    job_id: int
    user_id: int
    message: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 123,
                "job_id": 123,
                "user_id": 123,
                "message": "My message to employer",
            }
        }

        orm_mode = True


class ResponseInSchema(BaseModel):
    job_id: int
    message: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "job_id": 123,
                "message": "My message to employer",
            }
        }
