from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas_myinfo


def create_myinfo(db:Session, myinfo: schemas_myinfo.MyInfoCreate):
    new_myinfo = models.Myinfo(**myinfo.model_dump())
    db.add(new_myinfo)
    db.commit()
    db.refresh(new_myinfo)
    db.close()
    return new_myinfo


def get_myinfo_first(db: Session):
    return db.query(models.Myinfo).first()


def get_myinfo(db: Session, myinfo_id: int):
    return db.query(models.Myinfo).filter(models.Myinfo.id == myinfo_id).first()


def update_myinfo(db: Session, myinfo_id: int, updated_myinfo: schemas_myinfo.MyInfoUpdate):
    db_myinfo = get_myinfo(db, myinfo_id)
    if not db_myinfo:
        return None
    update_data = updated_myinfo.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_myinfo, key, value)
    db.add(db_myinfo)
    db.commit()
    db.refresh(db_myinfo)
    db.close()
    return db_myinfo
