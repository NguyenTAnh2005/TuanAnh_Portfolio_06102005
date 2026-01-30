from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.models import models
from app.db_connection import get_db
from app.core.security import get_current_user, get_current_admin
from app.schemas import schemas_system_config as schemas
from app.crud import crud_system_config as crud

router = APIRouter(
    prefix = "/system-config",
    tags = ["System Config Vippro"]
)


@router.post("/", response_model = schemas.SysConfResponse)
def create_sys_conf(
    sys_conf: schemas.SysConfCreate, 
    db : Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.create_sys_conf(db, sys_conf)


@router.get("/", response_model = list[schemas.SysConfResponse])
def get_all_sys_confs(
    skip: int = Query( 0, ge = 0),
    limit: int = Query(10, ge = 1, le = 10),
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.get_all_sys_confs(db, skip, limit)


@router.get("/{sys_conf_id}", response_model = schemas.SysConfResponse)
def get_sys_conf(
    sys_conf_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.get_sys_conf(db, sys_conf_id)


@router.put("/{sys_conf_id}", response_model = schemas.SysConfResponse)
def update_sys_conf(
    sys_conf_id: int,
    updated_sys_conf: schemas.SysConfUpdate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.update_sys_conf(db, sys_conf_id, updated_sys_conf)


@router.delete("/{sys_conf_id}")
def delete_sys_conf(
    sys_conf_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.delete_sys_conf(db, sys_conf_id)
