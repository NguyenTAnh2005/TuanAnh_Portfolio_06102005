from fastapi import HTTPException, status
from typing import Union
from app.core.security import get_current_user, get_current_admin
from app.models import models
from app.schemas import schemas_project
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.core.github_service import get_reposity_info
from app.core.security import parse_github_date
from datetime import datetime, timezone


def check_conflict(db: Session, project_id: int, 
                   object_project: Union[schemas_project.ProjectCreate, schemas_project.ProjectUpdate]
):
    filters = []
    if hasattr(object_project, "title") and object_project.title:
        filters.append(models.Project.title == object_project.title)
    if not filters:
        return 
    query = db.query(models.Project).filter(*filters)
    if project_id is not None:
        query = query.filter(models.Project.id != project_id)
    project_conflict = query.first()
    if project_conflict:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Đã tồn tại tên dự án trong cơ sở dữ liệu"
        )
    return 


async def create_project(db: Session, project: schemas_project.ProjectCreate):
    check_conflict(db, project_id = None, object_project = project)
    data_fetch = await get_reposity_info(project.project_url)

    # when GitHub API fail or repo url is invalid, we will set default values to avoid error :v 
    description = "No description provided"
    final_tech = project.tech_stack.copy()
    created_at = datetime.now(timezone.utc)
    last_updated = datetime.now(timezone.utc)
    if data_fetch:
        if data_fetch.get("description"):
            description = data_fetch["description"]
        created_at =  parse_github_date(data_fetch["created_at"])
        last_updated = parse_github_date(data_fetch["last_updated"])
        for tech in data_fetch["tech_stack"]:
            if tech not in final_tech:
                final_tech.append(tech)
    new_project = models.Project(
        title = project.title,
        description = description,
        thumbnail_url = project.thumbnail_url,
        project_url = project.project_url,
        deploy_url = project.deploy_url,
        tech_stack = final_tech,
        created_at = created_at,
        last_updated = last_updated
    )
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
        order: str = "desc" 
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


async def update_project(db: Session, project_id: int, updated_project: schemas_project.ProjectUpdate):
    check_conflict(db, project_id, object_project = updated_project)
    db_project = get_project(db, project_id)
    # Convert info at request first, and then, we will check the project_url
    update_data = updated_project.model_dump(exclude_unset = True)
    #If the project_url is updated, we need to fetch data from GitHub again
    new_url = update_data.get("project_url")
    if new_url and new_url != db_project.project_url:
        # Lấy tech_stack hiện tại (ưu tiên cái user vừa nhập trong request, nếu không có thì lấy từ DB)
        # Vì Schema có default=[], nên ta check xem nó có trong update_data không
        current_tech = update_data.get("tech_stack", db_project.tech_stack.copy())
        data_fetch = await get_reposity_info(new_url)
        if data_fetch.get("description"):
            update_data["description"] = data_fetch["description"]
        else: 
            update_data["description"] = "No description provided"
        update_data["created_at"] = parse_github_date(data_fetch["created_at"])
        update_data["last_updated"] = parse_github_date(data_fetch["last_updated"])
        for tech in data_fetch["tech_stack"]:
            if tech not in current_tech:
                current_tech.append(tech)
        update_data["tech_stack"] = current_tech
    for key, value in update_data.items():
        setattr(db_project, key, value)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    db.delete(db_project)
    db.commit()
    return {
        "status": "Success",
        "message": " Đã xóa thành công project",
        "project_info":db_project
    }
