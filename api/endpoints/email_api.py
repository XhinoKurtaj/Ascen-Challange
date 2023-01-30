from typing import List, Any
from fastapi import APIRouter, HTTPException, status, Depends,  Path
from sqlalchemy.orm import Session
from api import deps
from databases import Database
from schemas.email import EmailSchema
from api.deps import get_db
from crud import crud
from starlette.responses import JSONResponse
import pandas as pd
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import smtplib
from email.mime.text import MIMEText
import os 
from dotenv import load_dotenv
load_dotenv('.env')

router = APIRouter()


@router.post('/send-email')
def send_mail(email: EmailSchema, db: Session = Depends(get_db)) -> JSONResponse:
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    recipient_email = email.email
    subject = "PDF Raport"
    logs = [x.__dict__ for x in crud.get_logs_filter(db, email.date_range)]
    df = pd.DataFrame.from_records(logs)
    df = df.iloc[: , 1:]
    html = df.to_html()
    
    body = f"""<html>
        <body>
            {html}
        </body>
    </html>
    """
    html_message = MIMEText(body, 'html')
    html_message['Subject'] = subject
    html_message['From'] = sender_email
    html_message['To'] = recipient_email
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, html_message.as_string())
    server.quit()
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
    