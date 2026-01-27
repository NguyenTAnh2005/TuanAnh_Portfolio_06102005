from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import schemas_category_blog as schemas
from app.models import models
from sqlalchemy import or_


def create_category_blog(db: Session, category_blog: schemas.CategoryBlogCreate):
    new_name = category_blog.name
    new_slug = category_blog.slug
    db_category_blog = db.query(models.CategoryBlog).filter(or_(
        models.CategoryBlog.name == new_name,
        models.CategoryBlog.slug == new_slug
        )).first()
    if db_category_blog:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Category Blog đã tồn tại trường name hoặc slug. Vui lòng chỉnh sửa lại!"
        )
    new_category = models.CategoryBlog(**category_blog.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def get_all_category_blogs(
        db: Session, skip: int = 0, limit: int = 30, name: str = None
):
    query = db.query(models.CategoryBlog)
    if name:
        query = query.filter(models.CategoryBlog.name.ilike(f"%{name}%"))
    return query.offset(skip).limit(limit).all()


def get_category_blog( db: Session, category_blog_slug: str):
    db_category_blog = db.query(models.CategoryBlog).filter(models.CategoryBlog.slug == category_blog_slug).first()
    if not db_category_blog:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy đối tượng CategoryBlog trong hệ thống!"
        )
    return db_category_blog


def update_category_blog(db: Session, category_blog_id: int, updated_category_blog: schemas.CategoryBlogUpdate,):
    db_category_blog = get_category_blog(db, category_blog_id)
    update_data = updated_category_blog.model_dump(exclude_unset = True)
    for key, value in update_data.items():
        setattr(db_category_blog, key, value)
    db.add(db_category_blog)
    db.commit()
    db.refresh(db_category_blog)
    

def delete_category_blog(db: Session, category_blog_id: int):
    db_category_blog = get_category_blog(db, category_blog_id)
    # Because in models.py, we have set cascade for CategoryBlog, so when we delete CategoryBlog,
    # all blogs under this category will be deleted automatically. Amzingggg
    db.delete(db_category_blog)
    db.commit()

    return {
        "status": "Success",
        "message": " Đã xóa thành công categoryblog và các blog con liên quan",
        "category_info":{db_category_blog}
    }

