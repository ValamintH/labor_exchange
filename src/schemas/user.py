import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr


class UserSchema(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    hashed_password: str
    is_company: bool
    created_at: datetime.datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 123,
                "name": "John Smith",
                "email": "johnsmith@mail.com",
                "hashed_password": "$2b$12$AfEDs...",
                "is_company": False,
                "created_at": "2022-08-13T12:43:49.257481",
            }
        }

        orm_mode = True


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_company: Optional[bool] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "John Smith",
                "email": "johnsmith@mail.com",
                "is_company": False,
            }
        }


class UserInSchema(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str
    is_company: bool = False

    class Config:
        schema_extra = {
            "example": {
                "name": "John Smith",
                "email": "johnsmith@mail.com",
                "password": "8charactersMin",
                "password2": "8charactersMin",
                "is_company": False,
            }
        }

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values["password"]:
            raise ValueError("Пароли не совпадают!")
        return True
