from fastapi import APIRouter, Depends, Query 
from sqlalchemy.orm import Session
from typing import Literal
from app.core.security import get_current_user, get_current_admin
from app.db_connection import get_db
from app.schemas import schemas_project
from app.models import models
from app.crud import crud_project

router = APIRouter(
    prefix = "/projects",
    tags = ["Projects"]
)


@router.post("/", response_model = schemas_project.ProjectResponse)
async def create_project(
    project: schemas_project.ProjectCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return await crud_project.create_project(db, project = project)


@router.get("/", response_model = list[schemas_project.ProjectResponse])
def get_all_projects(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge = 0, description = "Số bản ghi muốn bỏ qua (trang 1 ... 10) "),
    limit: int = Query(30, ge = 1, le = 30, description = "Số dữ liệu (row) tối đa trên một trang"),
    title: str = Query(None, description = "Tìm theo tên dự án - description"),
    tech: str = Query(None, description = "Tìm theo tên công nghệ được sửa dụng trong dự án (React, FastAPI,...)"),
    sort_by: str = Query("created_at", description = "Sắp xếp theo cột nào trong CSDL"),
    order: Literal["asc", "desc"] = Query("desc", description = " Sắp xếp theo tăng dần (asc) hoặc giảm dần (desc)" )
):
    return crud_project.get_all_projects(db, skip = skip, limit = limit, title = title, tech = tech, sort_by = sort_by, order = order)


@router.get("/{project_id}", response_model = schemas_project.ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud_project.get_project(db, project_id = project_id)


@router.put("/{project_id}", response_model = schemas_project.ProjectUpdate)
async def update_project(
    project_id: int,
    updated_project: schemas_project.ProjectUpdate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return await crud_project.update_project(db, project_id = project_id, updated_project = updated_project)


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
): 
    return crud_project.delete_project(db, project_id = project_id)
    
    
