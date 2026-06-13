from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models.sensor import SensorReading
from app.schemas import SensorData

from app.services.state_engine import calculate_machine_state
from app.services.alert_service import create_alert

router = APIRouter()


# ----------------------------
# POST SENSOR DATA
# ----------------------------
@router.post("/sensor-data")
def receive_sensor_data(data: SensorData, db: Session = Depends(get_db)):

    turbidity = data.turbidity

    # Basic quality classification
    if turbidity < 1200:
        quality = "GOOD"
    elif turbidity < 2500:
        quality = "MEDIUM"
    else:
        quality = "RISKY"

    # Save to DB
    reading = SensorReading(
        machine_id=data.machine_id,
        turbidity=turbidity,
        quality_state=quality
    )

    db.add(reading)
    db.commit()
    db.refresh(reading)

    # ----------------------------
    # GET LAST 10 READINGS FOR TREND
    # ----------------------------
    history = db.query(SensorReading)\
        .filter(SensorReading.machine_id == data.machine_id)\
        .order_by(desc(SensorReading.id))\
        .limit(10)\
        .all()

    values = [h.turbidity for h in reversed(history)]

    # MACHINE STATE ENGINE
    state_result = calculate_machine_state(values)

    # ALERT SYSTEM (FIXED LOCATION)
    create_alert(db, data.machine_id, state_result)

    return {
        "id": reading.id,
        "machine_id": reading.machine_id,
        "turbidity": reading.turbidity,
        "quality_state": quality,
        "machine_state": state_result["state"],
        "risk_score": state_result["risk_score"],
        "trend": state_result["trend"]
    }


# ----------------------------
# HISTORY API (LAST 50 READINGS)
# ----------------------------
@router.get("/history/{machine_id}")
def get_history(machine_id: str, db: Session = Depends(get_db)):

    data = db.query(SensorReading)\
        .filter(SensorReading.machine_id == machine_id)\
        .order_by(desc(SensorReading.id))\
        .limit(50)\
        .all()

    return [
        {
            "turbidity": d.turbidity,
            "timestamp": d.timestamp,
            "quality_state": d.quality_state
        }
        for d in data
    ]