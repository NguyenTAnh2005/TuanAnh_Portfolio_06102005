from fastapi import HTTPException, status, Depends, APIRouter, Query
from sqlalchemy.orm import Session
from app.db_connection import get_db
from app.models import models
from app.schemas import schemas_category_blog as schemas
from app.crud import crud_category_blog as crud
from app.core.security import get_current_user, get_current_admin

router = APIRouter(
    prefix = "/category-blog",
    tags = ["Category Blog"]
)


@router.post("/create", response_model = schemas.CategoryBlogCreate)
def create_category_blog(
    category_blog: schemas.CategoryBlogCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.create_category_blog(db, category_blog)


@router.get("/get-all", response_model = list[schemas.CategoryBlogResponse])
def get_all_category_blogs(
    db: Session = Depends(get_db),
    name: str = Query(None, description = "Lọc theo tên"),
    skip: int = Query(0, ge = 0, description = "Number of page (++ 1) (eg: 0--1, 1--2, 2--3,...):"),
    limit: int = Query(20, ge = 1, le = 20, description = "Size of Page (eg: 15, 20,...)"),
    current_admin: models.User = Depends(get_current_admin)
    ):
    return crud.get_all_category_blogs(db, skip, limit, name)


@router.get("/get", response_model = schemas.CategoryBlogResponse)
def get_category_blog(
    slug: str,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.get_category_blog(db, slug)


@router.put("/update", response_model = schemas.CategoryBlogUpdate)
def update_category_blog(
    updated_category_blog: schemas.CategoryBlogUpdate,
    category_blog_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.update_category_blog(db, category_blog_id, updated_category_blog)


@router.delete("/delete")
def delete_category_blog(
    category_blog_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.delete_category_blog(db, category_blog_id)