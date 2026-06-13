from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database import Base


class MachineState(Base):
    __tablename__ = "machine_state"

    id = Column(Integer, primary_key=True, index=True)

    machine_id = Column(String, index=True)

    state = Column(String)

    risk_score = Column(Float)

    trend = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)