from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas_user
from app.crud import crud_user
from app.db_connection import get_db
from app.core.security import get_current_user, get_current_admin

router = APIRouter(
    prefix = "/user",
    tags = ["User"]
)


@router.post("/create-by-admin", response_model = schemas_user.UserCreateByAdmin)
def create_user_by_admin(
    user: schemas_user.UserCreateByAdmin,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud_user.create_user_by_admin(db, user)
 
# This Website don't have to register new user by themself, just sign in with Admin to edit info
# @router.post("/create-register")

# Admin in this website don't have to manage users
# @router.get("/get")
# @router.get("/get-all")

# @router.update--- for user, in current, we don't need this

@router.put("/update-by-admin/{user_id}", response_model = schemas_user.UserUpdateByAdmin)
def update_user_by_admin(
    user_id: int,
    user_update: schemas_user.UserUpdateByAdmin,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud_user.update_user_by_admin(db, user_id, user_update)


@router.patch("/update-password-by-admin/{user_id}", response_model = schemas_user.UserResponse)
def update_password_by_admin(
    password: schemas_user.UserUpdatePassWordAdmin,
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud_user.update_password_by_admin(db, user_id, password)


# @router.delete ----- this website also don't have to delete user :)))