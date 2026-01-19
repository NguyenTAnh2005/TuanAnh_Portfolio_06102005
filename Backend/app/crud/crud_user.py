from sqlalchemy.orm import Session
from app.models import models
from schemas import schemas_user

def create_user(db: Session, user: schemas_user.UserCreate):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.close()


def create_user_by_admin(db:Session, user: schemas_user.UserCreateByAdmin):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.close()


def get_all_users(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def update_user(db: Session, user_id: int, updated_user: schemas_user.UserUpdate):
    db_user = get_user(user_id)
    if not db_user:
        return None
    updated_data = updated_user.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.close()
    return db_user


def update_user_by_admin(db: Session, user_id: int, updated_user: schemas_user.UserUpdateByAdmin):
    db_user = get_user(user_id)
    if not db_user:
        return None
    updated_data = updated_user.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.close()
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    db.close()
    return db_user