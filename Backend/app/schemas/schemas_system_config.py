from pydantic import BaseModel, ConfigDict
from typing import Optional

class SysConfBase(BaseModel):
    config_key: str
    config_value: str


class SysConfCreate(SysConfBase):
    pass


class SysConfResponse(SysConfBase):
    id: int
    model_config = ConfigDict(from_attributes = True)


class SysConfUpdate(BaseModel):
    config_key:  Optional[str] = None
    config_value:  Optional[str] = None