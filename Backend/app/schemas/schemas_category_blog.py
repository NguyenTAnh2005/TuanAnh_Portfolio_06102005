from pydantic import BaseModel, ConfigDict
from typing import Optional

class CategoryBlogBase(BaseModel):
    name: str
    description: str
    slug: str

class CategoryBlogCreate(CategoryBlogBase):
    pass

class CategoryBlogResponse(CategoryBlogBase):
    id: int
    model_config = ConfigDict(from_attributes = True)

class CategoryBlogUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
