from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    password: str
    email: str


class UserCreate(UserBase):
    pass


class UserCreateByAdmin(UserBase):
    role_id: int


class UserRessponse(BaseModel):
    id: int
    class Config:
        from_attribute = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None


class UserUpdateByAdmin(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    role_id: Optional[int] = None
