from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class BlogBase(BaseModel):
    title : str
    summary : str
    content : str
    category_blog_id : int
    status :  str = "pending"
    slug : str
    thumbnail_url : str

class BlogCreate(BlogBase):
    pass

class BlogResponse(BlogBase):
    id: int
    created_at : datetime
    last_updated : datetime
    model_config = ConfigDict(from_attributes = True)


class BlogUpdate(BaseModel):
    title : Optional[str] = None
    summary : Optional[str] = None
    content : Optional[str] = None
    category_blog_id : Optional[int] = None
    created_at : Optional[datetime] = None
    # last_updated : Optional[datetime] = None
    status : Optional[str] = None
    slug : Optional[str] = None
    thumbnail_url : Optional[str] = None