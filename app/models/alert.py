from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    machine_id = Column(String, index=True)

    message = Column(String)

    risk_score = Column(Float)

    state = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)