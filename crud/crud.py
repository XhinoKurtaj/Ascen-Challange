from sqlalchemy.orm import Session

from model import models
from schemas import time_log as schema
from fastapi.encoders import jsonable_encoder
from typing import Union, Dict, Any
from schemas.time_log import UpdateLog, TimeLogDBBase
from schemas.email import PDFSchema


def get_log(db: Session, log_id: int):
    return db.query(models.TimeLog).filter(models.TimeLog.id == log_id).first()

def get_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TimeLog).offset(skip).limit(limit).all()

def get_logs_filter(db: Session, pdf: PDFSchema):
    return db.query(models.TimeLog).filter(
        models.TimeLog.date.between(pdf.start_date,  pdf.end_date)
    )

def store_log(db: Session, log: schema.CreateTimeLog):
    log.tags = ', '.join([str(elem) for elem in log.tags])
    db_log = models.TimeLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def update(db: Session, db_obj: TimeLogDBBase, obj_in: Union[UpdateLog, Dict[str, Any]]):

    obj_data = jsonable_encoder(db_obj)
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db_obj.tags = ', '.join([str(elem) for elem in db_obj.tags])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove_log(db: Session,  id: int):
    obj = db.query(models.TimeLog).get(id)
    db.delete(obj)
    db.commit()
    return obj