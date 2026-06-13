from pydantic import BaseModel


class SensorData(BaseModel):
    machine_id: str
    turbidity: float