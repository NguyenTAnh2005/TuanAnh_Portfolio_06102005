from pydantic import BaseModel
from typing import List, Optional, Dict

class MyInfoBase(BaseModel):
    fullname: str
    gender: str
    hometown: str
    major: str
    languages: List[str]
    frameworks: List[str]
    social_links: Dict[str, str]
    bio: str
    introduction: str

class MyInfoCreate(MyInfoBase):
    pass

class MyInfoResponse(MyInfoBase):
    id: int
    class Config:
        from_attributes = True 

class MyInfoUpdate(BaseModel):
    fullname: Optional[str] = None
    gender: Optional[str] = None
    hometown: Optional[str] = None
    major: Optional[str] = None
    languages: Optional[List[str]] = None
    frameworks: Optional[List[str]] = None 
    social_links: Optional[Dict[str, str]] = None 
    bio: Optional[str] = None
    introduction: Optional[str] = None
 
