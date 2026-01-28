from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from app.db_connection import get_db
from app.models import models
from app.schemas import schemas_role
from app.crud import crud_role
from app.core.security import get_current_user, get_current_admin


router = APIRouter(
    prefix = "/roles",
    tags = ["Role"]
)

@router.post("/", response_model = schemas_role.RoleCreate)
def create_role(
    role: schemas_role.RoleCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud_role.create_role(db, role = role)


@router.get("/", response_model = list[schemas_role.RoleResponse])
def get_all_roles(
    skip: int = Query(0, ge = 0, description = "Số bản ghi bỏ qua"), 
    limit: int = Query(30,ge = 1, le = 30, description = "Số bản ghi mỗi lần load lên"),
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud_role.get_all_roles(db, skip = skip, limit = limit)


@router.get("/{role_id}", response_model = schemas_role.RoleResponse)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    founded_role = crud_role.get_role(db, role_id = role_id)
    if not founded_role:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy dữ liệu!"
        )
    return founded_role

@router.put("/{role_id}", response_model = schemas_role.RoleUpdate)
def update_role(
    role_id: int,
    updated_role: schemas_role.RoleUpdate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    updated_data = crud_role.update_role(db, role_id = role_id, updated_role = updated_role)
    if not updated_data:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = " Không tìm thấy thông tin để cập nhật"
        )
    return updated_data


@router.delete("/{role_id}", response_model = schemas_role.RoleResponse)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    deleted_data = crud_role.delete_role(db, role_id = role_id)
    if not deleted_data:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy thông tin để xóa!"
        )
    return deleted_data
