from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import models
from app.schemas import schemas_timeline as schemas


def create_timeline(db: Session, timeline: schemas.TimelineCreate):
    db_sort_order = db.query(models.Timeline).filter(models.Timeline.sort_order == timeline.sort_order).first()
    if not db_sort_order:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Đã tồn tại trường sort_order, vui lòng chỉnh lại trường này!"
        )
    new_timeline = models.Timeline(**timeline.model_dump())
    db.add(new_timeline)
    db.commit()
    db.refresh(new_timeline)
    return new_timeline


def get_all_timelines(
        db: Session,
        skip: int,
        limit: int,
        title: str = None,
):
    query = db.query(models.Timeline)
    if title:
        query = query.filter(models.Timeline.title.ilike(f"%{title}%"))
    return query.offset(skip).limit(limit).all()


def get_timeline(
    db: Session,
    timeline_id: int
):
    db_timeline = db.query(models.Timeline).filter(models.Timeline.id == timeline_id).first()
    if not db_timeline:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Không tìm thấy đối tượng timeline trong hệ thống!"
        )
    return db_timeline


def update_timeline(
    db: Session,
    timeline_id: int,
    updated_timeline: schemas.TimelineUpdate
):
    db_timeline = get_timeline(db, timeline_id = timeline_id)
    update_data = updated_timeline.model_dump(exclude_unset = True)
    for key, value in update_data.items():
        setattr(db_timeline, key, value)
    db.add(db_timeline)
    db.commit()
    db.refresh(db_timeline)
    return db_timeline


def delete_timeline(db: Session, timeline_id: int):
    db_timeline = get_timeline(db, timeline_id = timeline_id)
    db.delete(db_timeline)
    db.commit()
    return {
        "status" : "Ok",
        "message" : f"Đã xóa thành công timeline có id {timeline_id}",
        "blog_info": db_timeline
    }