from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio

from database import engine, SessionLocal
from models import Base, Machine
from simulator import get_sensor_reading, inject_failure, reset_machine, generate_sensor_data
from agents.workflow import run_investigation
from agents.alert_agent import send_whatsapp_alert

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ADIAP Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "ADIAP Backend Running Successfully"}

@app.get("/machines")
def get_machines():
    db = SessionLocal()
    machines = db.query(Machine).all()
    db.close()
    result = []
    for m in machines:
        reading = get_sensor_reading(m.machine_id)
        result.append({
            "id":           m.machine_id,
            "machine_id":   m.machine_id,
            "machine_type": m.machine_type,
            "status":       reading["mode"],
            "sensors":      reading,
            "health_score": max(0, round(100 - reading["anomaly_score"], 1)),
        })
    return result

@app.get("/sensor-data")
def sensor_data():
    return generate_sensor_data()

@app.get("/sensor-data/{machine_id}")
def sensor_data_by_machine(machine_id: str):
    return get_sensor_reading(machine_id)

class FailureRequest(BaseModel):
    machine_id:   str
    failure_type: str

@app.post("/inject-failure")
async def inject_failure_route(req: FailureRequest, bg: BackgroundTasks):
    valid = ["bearing_wear", "lubrication_failure", "misalignment", "motor_overload"]
    if req.failure_type not in valid:
        return {"error": f"Choose from: {valid}"}
    inject_failure(req.machine_id, req.failure_type)
    bg.add_task(run_investigation_background, req.machine_id)
    return {"status": "injected", "machine_id": req.machine_id, "failure_type": req.failure_type}

async def run_investigation_background(machine_id: str):
    await asyncio.sleep(3)
    reading = get_sensor_reading(machine_id)
    report  = run_investigation(machine_id, reading["temperature"], reading["vibration"], reading["current"])
    await send_whatsapp_alert(report["whatsapp_message"])

@app.post("/reset-machine/{machine_id}")
def reset_machine_route(machine_id: str):
    reset_machine(machine_id)
    return {"status": "reset", "machine_id": machine_id}

@app.get("/investigation/{machine_id}")
def get_investigation(machine_id: str):
    reading = get_sensor_reading(machine_id)
    return run_investigation(machine_id, reading["temperature"], reading["vibration"], reading["current"])

@app.get("/business-impact/{machine_id}")
def get_business_impact(machine_id: str):
    reading = get_sensor_reading(machine_id)
    report  = run_investigation(machine_id, reading["temperature"], reading["vibration"], reading["current"])
    return report["business_impact"]

class AlertRequest(BaseModel):
    machine_id: str

@app.post("/send-alert")
async def send_alert(req: AlertRequest):
    reading = get_sensor_reading(req.machine_id)
    report  = run_investigation(req.machine_id, reading["temperature"], reading["vibration"], reading["current"])
    result  = await send_whatsapp_alert(report["whatsapp_message"])
    return {"status": "sent", "message": report["whatsapp_message"], "whatsapp_result": result}
