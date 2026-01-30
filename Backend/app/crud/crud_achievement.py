from fastapi import HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from typing import Union
from app.models import models
from app.schemas import schemas_achievement as schemas
from app.core.security import get_current_user, get_current_admin
from app.crud import crud_category_achievement as crud_ach


def check_conflict(
        db: Session, ach_id: int, 
        obj_ach: Union[schemas.AchCreate, schemas.AchUpdate]
):
    filters = []
    if hasattr(obj_ach, "category_achievements_id") and obj_ach.category_achievements_id is not None:
        crud_ach.get_category_ach(db, obj_ach.category_achievements_id)
        # Nếu không có category_achievements sẽ tự hiện lỗi hàm này, ko cần raise ở đây 
    if hasattr(obj_ach, "sort_order") and obj_ach.sort_order:
        filters.append(models.Achievement.sort_order == obj_ach.sort_order)
    if not filters:
        return 
    query = db.query(models.Achievement).filter(or_(*filters))
    if ach_id is not None:
        query = query.filter(models.Achievement.id != ach_id)
    conflict_data = query.first()
    if conflict_data:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Trường sort_order đã tồn tại trong hệ thống, vui lòng chỉnh sửa lại!"
        )
    return


def create_ach(db: Session, ach: schemas.AchCreate):
    check_conflict(db, ach_id = None, obj_ach = ach)
    new_ach = models.Achievement(**ach.model_dump())
    db.add(new_ach)
    db.commit()
    db.refresh(new_ach)
    return new_ach


def get_all_achs(db: Session, skip: int, limit: int, order: str):
    query = db.query(models.Achievement)
    if order == "asc":
        query = query.order_by(asc(models.Achievement.sort_order))
    # Sẽ cấu hình endpoint dạng enum chỉ 2 gtri asc - desc 
    query = query.order_by(asc(models.Achievement.sort_order))
    return query.offset(skip).limit(limit).all()


def get_ach(db: Session, ach_id: int):
    db_ach = db.query(models.Achievement).filter(models.Achievement.id == ach_id).first()
    if not db_ach:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy đối tượng Achievement trong hệ thống!"
        )
    return db_ach


def update_ach(db: Session, ach_id:int, updated_ach: schemas.AchUpdate):
    db_ach = get_ach(db, ach_id)
    check_conflict(db, ach_id, obj_ach = updated_ach)
    updated_data = updated_ach.model_dump(exclude_unset = True)
    for key, value in updated_data:
        setattr(db_ach, key, value)
    db.add(db_ach)
    db.commit()
    db.refresh(db_ach)
    return  db_ach


def delete_ach(db: Session, ach_id:int):
    db_ach = get_ach(db, ach_id)
    db.delete(db_ach)
    db.commit()
    return {
        "status" : "Ok",
        "message" : f"Đã xóa thành công  Achievemant có id {ach_id}",
        "blog_info": db_ach
    }


    
    
        