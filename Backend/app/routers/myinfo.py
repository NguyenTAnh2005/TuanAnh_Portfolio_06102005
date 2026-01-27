from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db_connection import get_db
from app.models import models
from app.schemas import schemas_myinfo
from app.crud import crud_myinfo
from app.core.security import get_current_user, get_current_admin

router = APIRouter(
    prefix = "/my-infos",
    tags = ["Info"]
)

@router.post("/", response_model = schemas_myinfo.MyInfoCreate)
def create_myinfo(
    myinfo: schemas_myinfo.MyInfoCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin) 
):
    count = db.query(models.Myinfo).count()
    if count >=1:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Đã tồn tại dữ liệu My info, hãy chạy API update"
        )
    return crud_myinfo.create_myinfo(db, myinfo = myinfo)


@router.get("/", response_model = schemas_myinfo.MyInfoResponse)
def get_myinfo_first(
    db: Session = Depends(get_db)
):
    return crud_myinfo.get_myinfo_first(db)


@router.get("/{id}", response_model = schemas_myinfo.MyInfoResponse)
def get_myinfo(
    id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud_myinfo.get_myinfo(db, myinfo_id = id)


@router.put("/{id}", response_model = schemas_myinfo.MyInfoUpdate)
def update_myinfo(
    id: int,
    updated_myinfo: schemas_myinfo.MyInfoUpdate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    updated_data = crud_myinfo.update_myinfo(db, myinfo_id = id, updated_myinfo = updated_myinfo)

    if not updated_data:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy thông tin để cập nhật!"
        )
    return updated_data

