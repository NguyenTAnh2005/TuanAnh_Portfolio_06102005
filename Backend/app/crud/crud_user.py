from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas_user
from fastapi import status, HTTPException
from app.core.security import hashing_password, checking_pasword
from app.core.config import settings
from sqlalchemy import or_

def create_user(db: Session, user: schemas_user.UserCreate):
    new_email = user.email
    db_user = db.query(models.User).filter(models.User.email == new_email).first()
    if db_user:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Email người dùng đã tồn tại. Vui lòng đổi email khác!"
        )
    new_user_data = user.model_dump()
    new_user_data["password"] = hashing_password(new_user_data["password"])
    new_user = models.User(**new_user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_user_by_admin(db:Session, user: schemas_user.UserCreateByAdmin):
    new_email = user.email
    db_user = db.query(models.User).filter(models.User.email == new_email).first()
    if db_user:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Email người dùng đã tồn tại. Vui lòng đổi email khác!"
        )
    new_user_data = user.model_dump()
    new_user_data["password"] = hashing_password(new_user_data["password"])
    new_user = models.User(**new_user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session, skip: int = 0, limit: int = 30):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy người dùng trong hệ thống!" 
        )
    return db_user


def update_user(db: Session, user_id: int, updated_user: schemas_user.UserUpdate):
    db_user = get_user(db, user_id)
    # If not db_user, thí function will raise HTTPExecption from get_user function abow
    # If user want to update password, hash it first
    if updated_user.password:
        updated_user.password = hashing_password(updated_user.password)
    updated_data = updated_user.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_by_admin(db: Session, user_id: int, updated_user: schemas_user.UserUpdateByAdmin):
    db_user = get_user(db, user_id)
    updated_data = updated_user.model_dump(exclude_unset=True)
    # admin can't update password for user so we don't need to hash password here
    for key, value in updated_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()
    # This user has been deleted so don't use db.refresh()
    return db_user


def update_password_by_admin(db: Session, user_id: int, password_object: schemas_user.UserUpdatePassWordAdmin):
    db_user = get_user(db, user_id)
    new_password = hashing_password(password_object.password)
    db_user.password = new_password
    db.commit()
    db.refresh(db_user)
    return db_user


def recovery_password_admin_account(db: Session):
    if not settings.FIRST_ADMIN_PASSWORD:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = " Pydantic Setting không đọc được mật khẩu từ env. Checking env file again!"
        )
    db_user = db.query(models.User).filter(
        or_(
            models.User.email == settings.FIRST_ADMIN_EMAIL,
             models.User.id == 1)
        ).first()
    if not db_user: 
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy tài khoản Admin ban đầu do không khớp email hoặc id"
        )
    db_user.password = hashing_password(settings.FIRST_ADMIN_PASSWORD)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Khôi phục lại mật khẩu thành công!"}