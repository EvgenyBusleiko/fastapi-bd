from pydantic import BaseModel, Field, EmailStr



class UserIn(BaseModel):
    username: str = Field(min_length=2)
    lastname: str = Field(min_length=2)
    email: EmailStr = Field(max_length=128)
    password: str = Field(min_length=5)


class User(UserIn):
    id: int