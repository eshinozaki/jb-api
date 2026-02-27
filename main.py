from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="JUNBELL AI Server")

class JunbellAlert(BaseModel):
    timestamp: str
    patient_name: str
    message: str
    alert_level: str
    frequency: str
    intensity: str
    notes_detected: str # now "E-E-E" 
@app.get("/")
def health():
    return {"status": "JUNBELL API running"}

@app.post("/classify")
def classify_alert(alert: JunbellAlert):
    # If you want server-side enforcement, uncomment below and map notes to level/message.
    # Otherwise, trust frontend and just echo back normalized.

    return {
        "timestamp": alert.timestamp,
        "patient_name": alert.patient_name,
        "message": alert.message,
        "alert_level": alert.alert_level,
        "frequency": alert.frequency,
        "intensity": alert.intensity,
        "notes_detected": alert.notes_detected
    }


