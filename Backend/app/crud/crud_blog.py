from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_
from app.models import models
from app.schemas import schemas_blog as schemas
from app.crud import crud_category_blog as crud_CB
from datetime import datetime

# CB = Category Blog


def create_blog(db: Session, blog: schemas.BlogCreate):
    db_CB = crud_CB.get_category_blog_by_id(blog.category_blog_id)
    check_title = db.query(models.Blog).filter(or_(models.Blog.slug == blog.slug, models.Blog.title == blog.title)).first()
    if check_title:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Trường title trong request đã tồn tại trong hệ thống! Vui lòng đổi title!"
        )
    # In database, I have set sever_default for created_at and onupdate for last_updated, so I don't need to set it here 
    new_blog = models.Blog(**blog.model_dump())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_all_blogs(
        db:Session, skip: int, limit: int, 
        title: str = None, category_blog_id: int = None,
        status: str = None, sort_column: str = "created_at", 
        order: str = "desc" 
    ):
    query = db.query(models.Blog)
    if title:
        query = query.filter(models.Blog.title.ilike(f"%{title}%"))
    if category_blog_id:
        query = query.filter(models.Blog.category_blog_id == category_blog_id)
    if status:
        query = query.filter(models.Blog.status == status)
    # Finding sort column based on getattr with input if not found, default is created_at
    sort_column_query = getattr(models.Blog, sort_column, models.Blog.created_at)
    if order == "desc":
        query = query.order_by(desc(sort_column_query))
    else:
        query = query.order_by(asc(sort_column_query))
    return query.offset(skip).limit(limit).all()

def get_blog_by_id(db: Session, blog_id: int):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not db_blog:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy đối tượng blog trong hệ thống!"
        )


def get_blog_by_slug(db: Session, blog_slug: str):
    db_blog = db.query(models.Blog).filter(models.Blog.slug == blog_slug).first()
    if not db_blog:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy đối tượng blog trong hệ thống!"
        )
    

def update_blog(db: Session, blog_id: int, updated_blog: schemas.BlogUpdate):
    db_blog = get_blog_by_id(db, blog_id)

