from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas_role
from fastapi import HTTPException, status
from typing import Union


def checking_conflig(db: Session, role_id: int, updated_role: Union[schemas_role.RoleUpdate, schemas_role.RoleCreate]):
    if role_id != None:
        role_conflig = db.query(models.Role).filter(
        models.Role.id != role_id,
        models.Role.name == updated_role.name,
        ).first()
    elif role_id == None:
        role_conflig = db.query(models.Role).filter(
        models.Role.name == updated_role.name,
        ).first()
    if role_conflig:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Trường name bị trùng với dữ liệu đã có sẵn, vui lòng kiểm tra lại!"
        )
    return 

def create_role(db: Session, role: schemas_role.RoleCreate):
    checking_conflig(db, role_id = None, updated_role = role)
    new_role = models.Role(**role.model_dump())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


def get_all_roles(db: Session, skip: int = 0, limit: int = 30):
    return db.query(models.Role).offset(skip).limit(limit).all()


def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def update_role(db: Session, role_id: int, updated_role: schemas_role.RoleUpdate):
    db_role = get_role(db, role_id)
    checking_conflig(db, role_id, updated_role)
    update_data = updated_role.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_role, key, value)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role



def delete_role(db: Session, role_id: int):
    db_role = get_role(role_id)
    db.delete(db_role)
    db.commit()
    return db_role
    