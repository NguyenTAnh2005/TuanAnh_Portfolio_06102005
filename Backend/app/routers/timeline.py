from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas import schemas_timeline as schemas
from app.crud import crud_timeline as crud
from app.models import models
from app.core.security import get_current_user, get_current_admin

router = APIRouter(
    prefix = "/time-line",
    tags = ["Time Line"]
)