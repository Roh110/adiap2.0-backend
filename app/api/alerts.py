from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models.alert import Alert

router = APIRouter()


@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):

    alerts = db.query(Alert)\
        .order_by(desc(Alert.id))\
        .limit(50)\
        .all()

    return [
        {
            "machine_id": a.machine_id,
            "message": a.message,
            "risk_score": a.risk_score,
            "state": a.state,
            "timestamp": a.timestamp
        }
        for a in alerts
    ]