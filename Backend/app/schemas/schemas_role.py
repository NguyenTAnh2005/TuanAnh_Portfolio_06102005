from pydantic import BaseModel
from typing import Optional

class RoleBase(BaseModel):
    name: str
    description: str


class RoleCreate(RoleBase):
    pass


class RoleResponse(RoleBase):
    id: int
    class Config:
        from_attribute = True


class RoleUpdate(BaseModel):
    # Các schemas Update ko bỏ id bên trong,
    # khi viết API endpoint mới đụng đến id sau 
    name: Optional[str] = None
    description: Optional[str] = None
