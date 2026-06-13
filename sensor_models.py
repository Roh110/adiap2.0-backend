from sqlalchemy import Column, Integer, Float, String
from database import Base


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)

    machine_id = Column(String)

    temperature = Column(Float)

    vibration = Column(Float)

    current = Column(Float)

    status = Column(String)