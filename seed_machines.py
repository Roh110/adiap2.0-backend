from database import SessionLocal
from models import Machine

db = SessionLocal()

machines = [
    Machine(
        machine_id="CNC-01",
        machine_type="CNC",
        status="Healthy"
    ),
    Machine(
        machine_id="PRESS-01",
        machine_type="Press",
        status="Healthy"
    ),
    Machine(
        machine_id="PUMP-01",
        machine_type="Pump",
        status="Healthy"
    )
]

for machine in machines:
    db.add(machine)

db.commit()

print("Machines Added Successfully")