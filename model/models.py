from sqlalchemy import Boolean, Column, Integer, String, Date
from db.session import Base


class TimeLog(Base):
    __tablename__ = "time_log"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String,  nullable=False)
    description = Column(String)
    project = Column(String, index=True)
    tags = Column(String)
