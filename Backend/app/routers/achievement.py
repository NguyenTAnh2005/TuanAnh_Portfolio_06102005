from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import Literal
from app.models import models
from app.db_connection import get_db
from app.core.security import get_current_user, get_current_admin
from app.schemas import schemas_achievement as schemas
from app.crud import crud_achievement as crud

router = APIRouter(
    prefix = "/achievements",
    tags = ["Achievement"]
)


@router.post("/", response_model = schemas.AchResponse)
def create_achievement(
    ach: schemas.AchCreate, 
    db : Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.create_ach(db, ach)


@router.get("/", response_model = list[schemas.AchResponse])
def get_all_achievements(
    skip: int = Query( 0, ge = 0),
    limit: int = Query(10, ge = 1, le = 10),
    order: Literal["asc", "desc"] = Query("desc", description = " Thứ tự sắp xếp tăng hay giảm: "),
    db: Session = Depends(get_db)
):
    return crud.get_all_achs(db, skip, limit, order)


@router.get("/{ach_id}", response_model = schemas.AchResponse)
def get_achievement(
    ach_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_ach(db, ach_id)


@router.put("/{ach_id}", response_model = schemas.AchResponse)
def update_achievement(
    ach_id: int,
    updated_ach: schemas.AchUpdate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.update_ach(db, ach_id, updated_ach)


@router.delete("/{ach_id}")
def delete_achievement(
    ach_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.delete_ach(db, ach_id)
