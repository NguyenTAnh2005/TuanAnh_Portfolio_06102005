from pydantic import BaseModel, ConfigDict
from typing import Optional

class CategoryAchBase(BaseModel):
    name: str
    description: str

class CategoryAchCreate(CategoryAchBase):
    pass

class CategoryAchResponse(CategoryAchBase):
    id: int
    model_config = ConfigDict(from_attributes = True)

class CategoryAchUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

