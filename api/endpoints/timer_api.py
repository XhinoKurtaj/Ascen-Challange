from typing import List, Any
from fastapi import APIRouter, HTTPException, status, Depends,  Path
from sqlalchemy.orm import Session
from api import deps
from databases import Database
from schemas.time_log import CreateTimeLog, Log, TimeLogDBBase, UpdateLog, TimeLogBase
from api.deps import get_db
from crud import crud

import pandas as pd
from starlette.responses import FileResponse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


router = APIRouter()

@router.post("/log/", response_model=TimeLogDBBase)
def create_user(log: CreateTimeLog, db: Session = Depends(get_db)):
    return crud.store_log(db=db, log=log)

@router.get("/log/", response_model=list[TimeLogDBBase])
def read_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = crud.get_logs(db, skip=skip, limit=limit)
    return logs

@router.get("/log/{id}", response_model=TimeLogDBBase)
def read_log(id: int = Path(..., ge=1), db: Session = Depends(get_db), ):
    logs = crud.get_log(db=db, log_id=id)
    return logs

@router.put("/log/{id}", response_model=Log)
def update_log(*, db: Session = Depends(deps.get_db), id: int, item_in: TimeLogBase) -> Any:
    item = crud.get_log(db=db, log_id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Log not found")
    item = crud.update(db=db, db_obj=item, obj_in=item_in)
    return item

@router.delete("/{id}", response_model=Log)
def delete_log(id: int, db: Session = Depends(deps.get_db)) -> Any:
    item = crud.get_log(db=db, log_id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Log not found")
    item = crud.remove_log(db=db, id=id)
    return item