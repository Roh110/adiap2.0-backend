from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime

from app.database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)

    machine_id = Column(String, index=True)

    turbidity = Column(Float)

    quality_state = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)