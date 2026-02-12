from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    thumbnail_url: str 
    project_url: str
    deploy_url: Optional[str] = None 
    tech_stack: list[str]  = []


class ProjectCreate(ProjectBase):
    created_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None

 
class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    last_updated: datetime
    # help Pydantic know to read data from ORM model,
    # beacuse by default Pydantic only reads data from dicts
    model_config = ConfigDict(from_attributes = True)


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    thumbnail_url: Optional[str] = None
    project_url: Optional[str] = None 
    deploy_url: Optional[str] = None 
    tech_stack: list[str]  = []

class ProjectPaginationResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: list[ProjectResponse]
