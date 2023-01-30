
from datetime import date 

from pydantic import BaseModel
from typing import List, Optional

from pydantic import BaseModel

class TimeLogBase(BaseModel):
    date       :   date
    start_time      :   str
    end_time        :   str
    description     :   Optional[str] = None
    project         :   str
    tags            :   Optional[List[str]] = None


class CreateTimeLog(TimeLogBase):
    pass


class UpdateLog(TimeLogBase):
    tags    :   str

class TimeLogDB(TimeLogBase):
    id      :   int

class TimeLogDBBase(TimeLogBase):
    id      :   int
    tags    :   str

    class Config:
        orm_mode    =   True

# Properties to return to client
class Log(TimeLogDBBase):
    pass


# Properties properties stored in DB
class LogInDB(TimeLogDBBase):
    pass