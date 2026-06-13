from sqlalchemy import Column, Integer, String
from database import Base


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, unique=True)
    machine_type = Column(String)
    status = Column(String)