from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import Literal
from app.models import models
from app.db_connection import get_db
from app.core.security import get_current_user, get_current_admin
from app.schemas import schemas_blog as schemas
from app.crud import crud_blog as crud


router = APIRouter(
    prefix = "/blogs",
    tags = ["Blog"]
)


@router.post("/", response_model = schemas.BlogCreate)
def create_blog(
    blog: schemas.BlogCreate,
    db: Session = Depends(get_db),
    current_admin : models.User = Depends(get_current_admin)
):
    return crud.create_blog(db, blog)


@router.get("/", response_model = list[schemas.BlogResponse])
def get_all_blogs(
    title: str = Query(None, description = "Lọc theo tên blog:"),
    category_blog_id: int = Query(None, description = "Lọc theo danh mục blog: "),
    status : str = Query(None, description = "Lọc theo trạng thái: "),
    sort_column : str = Query("created_at", description = "Sắp xếp theo thuộc tính nào: "),
    order: Literal["asc", "desc"] = Query("desc", description = "Sắp xếp theo tăng dần (asc) - giảm dần (desc):"),
    skip: int = Query(0, ge = 0, description = "Số trang muốn bỏ qua trong hệ thống phân trang (0 --> trang 1):"),
    limit: int = Query(20, ge = 1, le = 20, description = " Số lượng bài viết tối đa trên một trang: "),
    db: Session = Depends(get_db)
):
    return crud.get_all_blogs(db, skip, limit, title, category_blog_id, status, sort_column, order)



@router.get("/{blog_id:int}", response_model = schemas.BlogResponse)
def get_blog_by_id(
    blog_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    """
    a function for Admin to debug easier :v
    """
    return crud.get_blog_by_id(db, blog_id = blog_id)


@router.get("/{blog_slug}", response_model = schemas.BlogResponse)
def get_blog_by_Slug(
    blog_slug: str,
    db: Session = Depends(get_db)
):
    return crud.get_blog_by_slug(db, blog_slug = blog_slug)




@router.put("/{blog_id}", response_model = schemas.BlogResponse)
def update_blog(
    blog_id: int,
    updated_blog: schemas.BlogUpdate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.update_blog(db, blog_id = blog_id, updated_blog = updated_blog)


@router.delete("/{blog_id}")
def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    db_blog = crud.delete_blog(db, blog_id = blog_id)
    return db_blog
