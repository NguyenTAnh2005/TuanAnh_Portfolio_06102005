from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.models import models
from app.db_connection import get_db
from app.core.security import get_current_user, get_current_admin
from app.schemas import schemas_category_achievement as schemas
from app.crud import crud_category_achievement as crud


router = APIRouter(
    prefix = "/category-achievements",
    tags = ["Category Achievement"]
)


@router.post("/", response_model = schemas.CategoryAchResponse)
def create_category_ach(
    category_ach: schemas.CategoryAchCreate, 
    db : Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.create_category_ach(db, category_ach)


@router.get("/", response_model = list[schemas.CategoryAchResponse])
def get_all_category_achs(
    skip: int = Query( 0, ge = 0),
    limit: int = Query(10, ge = 1, le = 10),
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.get_all_category_achs(db, skip, limit)


@router.get("/{category_ach_id}", response_model = schemas.CategoryAchResponse)
def get_category_ach(
    category_ach_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_category_ach(db, category_ach_id)


@router.put("/{category_ach_id}", response_model = schemas.CategoryAchResponse)
def update_category_ach(
    category_ach_id: int,
    updated_category_ach: schemas.CategoryAchUpdate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.update_category_ach(db, category_ach_id, updated_category_ach)


@router.delete("/{category_ach_id}")
def delete_category_ach(
    category_ach_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.delete_category_ach(db, category_ach_id)

