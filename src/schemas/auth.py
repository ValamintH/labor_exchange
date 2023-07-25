from pydantic import BaseModel, EmailStr


class TokenSchema(BaseModel):
    access_token: str
    token_type: str

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciO...",
                "token_type": "Bearer",
            }
        }


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "johnsmith@mail.com",
                "password": "8charactersMin",
            }
        }
