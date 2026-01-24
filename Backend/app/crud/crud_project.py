from fastapi import HTTPException, status
from app.core.security import get_current_user, get_current_admin
from app.models import models
from app.schemas import schemas_project
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

def create_project(db: Session, project: schemas_project.ProjectCreate):
    db_project = db.query(models.Project).filter(models.Project.title == project.title).first()
    if db_project:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Đã tồn tại tên dự án trong cơ sở dữ liệu"
        )
    new_project = models.Project(**project.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


def get_all_projects(
        db: Session,
        skip: int = 0,
        limit: int = 30,
        title: str = None,
        tech: str = None,
        sort_by: str = "created_at",
        order: str = "desc" # tăng dần (small --> big)
        ):
    query = db.query(models.Project)
    if title:
        query = query.filter(models.Project.title.ilike(f"%{title}%"))
    if tech:
        query = query.filter(models.Project.tech_stack.contains([tech]))
    # Because we input string to sort and Python don't know this is column name, 
    # so we use getattr to get column from models.Project, and set default is created_at
    sort_column = getattr(models.Project, sort_by, models.Project.created_at)

    if order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))
    return query.offset(skip).limit(limit).all()


def get_project(db: Session, project_id: int):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy đối tượng Project trong hệ thống!"
        )
    return db_project


def update_project(db: Session, project_id: int, updated_project: schemas_project.ProjectUpdate):
    db_project = get_project(db, project_id)
    updated_data = updated_project.model_dump(exclude_unset = True)
    for key, value in updated_data.items():
       setattr(db_project, key, value)
    db.add(updated_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    db.delete(db_project)
    db.commit()
    return db_project
