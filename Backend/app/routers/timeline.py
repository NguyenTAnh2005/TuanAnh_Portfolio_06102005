from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db_connection import get_db
from app.schemas import schemas_timeline as schemas
from app.crud import crud_timeline as crud
from app.models import models
from app.core.security import get_current_user, get_current_admin

router = APIRouter(
    prefix = "/time-lines",
    tags = ["Time Line"]
)


@router.post("/", response_model = schemas.TimelineResponse)
def create_timeline(
    timeline: schemas.TimelineCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.create_timeline(db, timeline)


@router.get("/", response_model = list[schemas.TimelineResponse])
def get_all_timelines(
    title: str = Query(None, description = "Lọc timeline theo tên"),
    skip: int = Query(0, ge = 0, description = "Số trang muốn bỏ qua: "),
    limit: int = Query(10, ge = 1, le = 10, description = "Số lượng phần tử tối đa trên một trang:"),
    db: Session = Depends(get_db)
):
    return crud.get_all_timelines(db, skip, limit, title)


@router.get("/{timeline_id}", response_model = schemas.TimelineResponse)
def get_timeline(timeline_id: int, db: Session = Depends(get_db)):
    return crud.get_timeline(db, timeline_id)


@router.put("/{timeline_id}", response_model = schemas.TimelineResponse)
def update_timeline(
    timeline_id: int,
    updated_timeline: schemas.TimelineUpdate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):
    return crud.update_timeline(db, timeline_id, updated_timeline)


@router.delete("/{timeline_id}")
def delete_timeline(
    timeline_id: int, 
    db: Session = Depends(get_db), 
    current_admin: models.User = Depends(get_current_admin)
    ):
    return crud.delete_timeline(db, timeline_id)