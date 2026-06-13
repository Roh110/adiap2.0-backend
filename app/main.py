from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.api.sensor import router as sensor_router
from app.api.alerts import router as alert_router


app = FastAPI(
    title="ADIAP 2.0 - Agentic Data Intelligence for Asset Prediction",
    version="1.0.0"
)

# Create all database tables
Base.metadata.create_all(bind=engine)


# ----------------------------
# ROOT ENDPOINT
# ----------------------------
@app.get("/")
def root():
    return {
        "message": "ADIAP Backend Running"
    }


# ----------------------------
# REGISTER ROUTES
# ----------------------------
app.include_router(sensor_router)
app.include_router(alert_router)