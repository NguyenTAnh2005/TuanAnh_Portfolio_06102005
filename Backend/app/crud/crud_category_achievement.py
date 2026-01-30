from fastapi import HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Union
from app.models import models
from app.schemas import schemas_category_achievement as schemas
from app.core.security import get_current_user, get_current_admin


def check_conflict(
        db: Session, ca_id: int, 
        obj_ca: Union[schemas.CategoryAchCreate, schemas.CategoryAchUpdate]
    ):
    filters = []
    if hasattr(obj_ca, "name") and obj_ca.name:
        filters.append(models.CategoryAchievement.name == obj_ca.name)
    if not filters:
        return 
    query = db.query(models.CategoryAchievement).filter(or_(*filters))
    if ca_id is not None:
        query = query.filter(models.CategoryAchievement.id != ca_id)
    conflict_data = query.first()
    if conflict_data:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Đã tồn tại name CategoryAchievement trong hệ thống!"
        )
    return 

def create_category_ach(db: Session, category_ach: schemas.CategoryAchCreate):
    check_conflict(db, ca_id = None, obj_ca = category_ach)
    new_category_ach = models.CategoryAchievement(**category_ach.model_dump())
    db.add(new_category_ach)
    db.commit()
    db.refresh(new_category_ach)
    return new_category_ach


def get_all_category_achs(db: Session, skip: int, limit: int):
    return db.query(models.CategoryAchievement).offset(skip).limit(limit).all()


def get_category_ach(db: Session, category_ach_id: int):
    db_category_ach = db.query(models.CategoryAchievement).filter(models.CategoryAchievement.id == category_ach_id).first()
    if not db_category_ach:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy đối tượng Category Achievement trong hệ thống!"
        )
    return db_category_ach


def update_category_ach(db: Session, category_ach_id: int, updated_category_ach: schemas.CategoryAchUpdate):
    db_category_ach = get_category_ach(db, category_ach_id)
    check_conflict(db, ca_id =  category_ach_id, obj_ca = updated_category_ach)
    updated_data = updated_category_ach.model_dump(exclude_unset = True)
    for key, value in updated_data.items():
        setattr(db_category_ach, key, value)
    db.add(db_category_ach)
    db.commit()
    db.refresh(db_category_ach)
    return db_category_ach


def delete_category_ach(db: Session, category_ach_id: int):
    db_category_ach = get_category_ach(db, category_ach_id)
    db.delete(db_category_ach)
    db.commit()
    return {
        "status" : "Ok",
        "message" : f"Đã xóa thành công category Achievemant có id {category_ach_id}",
        "blog_info": db_category_ach
    }