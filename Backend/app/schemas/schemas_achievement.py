from pydantic import BaseModel, ConfigDict
from typing import Optional

class AchBase(BaseModel):
    title: str
    content: str
    achieved_at: str
    evidence_url: str
    sort_order: int
    category_achievements_id: int


class AchCreate(AchBase):
    pass


class AchResponse(AchBase):
    id: int
    model_config = ConfigDict(from_attributes = True)


class AchUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    achieved_at: Optional[str] = None
    evidence_url: Optional[str] = None
    sort_order: Optional[int] = None
    category_achievements_id: Optional[int] = None