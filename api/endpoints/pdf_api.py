from typing import List, Any, Optional
from fastapi import APIRouter, HTTPException, status, Depends,  Path
from sqlalchemy.orm import Session
from api import deps
from databases import Database
from schemas.time_log import CreateTimeLog, Log, TimeLogDBBase, UpdateLog, TimeLogBase
from api.deps import get_db
from crud import crud
from schemas.email import PDFSchema
import pandas as pd
from starlette.responses import FileResponse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

router = APIRouter()

@router.post("/generate-pdf")
def generate_pdf(pdf: Optional[PDFSchema] = None, db: Session = Depends(get_db)):
    logs = [x.__dict__ for x in crud.get_logs_filter(db, pdf)]
    if len(logs) > 0:
        df = pd.DataFrame.from_records(logs)
        df = df.iloc[: , 1:]
        fig, ax =plt.subplots(figsize=(12,4))
        ax.axis('tight')
        ax.axis('off')
        the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
        pp = PdfPages("raport.pdf")
        pp.savefig(fig, bbox_inches='tight')
        pp.close()
        return FileResponse(path='raport.pdf', media_type='application/octet-stream',filename='raport.pdf')