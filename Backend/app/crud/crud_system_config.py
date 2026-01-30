from fastapi import HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from typing import Union
from app.models import models
from app.schemas import schemas_system_config as schemas
from app.core.security import get_current_user, get_current_admin


def check_conflict(
        db: Session, sys_conf_id: int, 
        obj_sys_conf: Union[schemas.SysConfCreate, schemas.SysConfUpdate]
):
    filters = []
    if hasattr(obj_sys_conf, "config_key") and obj_sys_conf.config_key is not None:
        filters.append(models.SystemConfig.config_key == obj_sys_conf.config_key)
    if not filters:
        return 
    query = db.query(models.SystemConfig).filter(or_(*filters))
    if sys_conf_id is not None:
        query = query.filter(models.SystemConfig.id != sys_conf_id)
    conflict_data = query.first()
    if conflict_data:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Trường config name đã tồn tại trong hệ thống, vui lòng chỉnh sửa lại!"
        )
    return


def create_sys_conf(db: Session, sys_conf: schemas.SysConfCreate):
    check_conflict(db, sys_conf_id = None, obj_sys_conf = sys_conf)
    new_sys_conf = models.SystemConfig(**sys_conf.model_dump())
    db.add(new_sys_conf)
    db.commit()
    db.refresh(new_sys_conf)
    return new_sys_conf


def get_all_sys_confs(db: Session, skip: int, limit: int):
    query = db.query(models.SystemConfig)
    return query.offset(skip).limit(limit).all()


def get_sys_conf(db: Session, sys_conf_id: int):
    db_sys_conf = db.query(models.SystemConfig).filter(models.SystemConfig.id == sys_conf_id).first()
    if not db_sys_conf:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy đối tượng System Config trong hệ thống!"
        )
    return db_sys_conf


def update_sys_conf(db: Session, sys_conf_id:int, updated_sys_conf: schemas.SysConfUpdate):
    db_sys_conf = get_sys_conf(db, sys_conf_id)
    check_conflict(db, sys_conf_id, obj_sys_conf = updated_sys_conf)
    updated_data = updated_sys_conf.model_dump(exclude_unset = True)
    for key, value in updated_data.items():
        setattr(db_sys_conf, key, value)
    db.add(db_sys_conf)
    db.commit()
    db.refresh(db_sys_conf)
    return  db_sys_conf


def delete_sys_conf(db: Session, sys_conf_id:int):
    db_sys_conf = get_sys_conf(db, sys_conf_id)
    db.delete(db_sys_conf)
    db.commit()
    return {
        "status" : "Ok",
        "message" : f"Đã xóa thành công  System Config có id {sys_conf_id}",
        "blog_info": db_sys_conf
    }


    
    
        