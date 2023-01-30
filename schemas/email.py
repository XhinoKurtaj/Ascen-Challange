from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime, date, timedelta

current_date = datetime.today()

class PDFSchema(BaseModel):
    start_date  :   str     =   date.today()
    end_date    :   str     =   (current_date + timedelta(weeks=1)).date()

class EmailSchema(BaseModel):
    email       :   EmailStr
    date_range  :   PDFSchema
    
    
    