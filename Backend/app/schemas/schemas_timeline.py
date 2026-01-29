from pydantic import BaseModel, ConfigDict
from typing import Optional

class TimelineBase(BaseModel):
    title : str
    organization : str
    description : str
    start_end : str
    sort_order : int

class TimelineCreate(TimelineBase):
    pass

class TimelineResponse(TimelineBase):
    id: int
    model_config = ConfigDict(from_attributes = True)

class TimelineUpdate(BaseModel):
    title : Optional[str] = None
    organization : Optional[str] = None
    description : Optional[str] = None
    start_end : Optional[str] = None
    sort_order : Optional[int] = None