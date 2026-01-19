from sqlalchemy.orm import Session
from app.models import models
from schemas import schemas_role

def create_role(db: Session, role: schemas_role.RoleCreate):
    new_role = models.Role(**role.model_dump())
    db.add(new_role)
    db.commit()
    db.close()
    return new_role


def get_all_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()


def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def update_role(db: Session, role_id: int, updated_role: schemas_role.RoleUpdate):
    db_role = get_role(role_id)
    if not db_role:
        return None
    # Just update which from request update
    update_data = updated_role.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_role, key, value)
    db.add(db_role)
    db.commit()
    db.close()
    return db_role


def delete_role(db: Session, role_id: int):
    db_role = get_role(role_id)
    if not db_role:
        return None
    db.delete(db_role)
    db.commit()
    db.close()
    return db_role
    