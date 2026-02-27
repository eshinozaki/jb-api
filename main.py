from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="JUNBELL AI Server")

# Incoming JSON model
class JunbellAlert(BaseModel):
    patient_name: str
    note_sequence: str   # example: "E-E-E"
    sound_type: str
    frequency: str
    intensity: str
    timestamp: str


# Note classification map
NOTE_MAP = {
    "E": ("HELP!", "Urgent"),
    "C": ("Yes", "Normal"),
    "G": ("No", "Semi-Urgent"),

    "C-E": ("Water", "Non-Urgent"),
    "E-G": ("Food", "Non-Urgent"),
    "E-C": ("Bathroom", "Non-Urgent"),

    "E-E-E": ("Pain", "Urgent"),
    "C-G": ("Thank You", "Normal"),
    "G-C": ("Love You", "Normal"),
    "C-C": ("I'm Okay", "Normal"),

    "E-C-E": ("Watch TV", "Normal"),
    "C-C-C": ("Good Morning", "Non-Urgent"),
    "G-G-G": ("Good Night", "Non-Urgent"),

    "G-E": ("Tired", "Semi-Urgent"),
    "C-C-E": ("Where's Family", "Urgent"),
    "G-G": ("Medicine", "Semi-Urgent"),

    "C-G-C": ("Happy", "Normal"),
    "C-G-E": ("Sad", "Normal"),
    "C-G-G": ("Worried", "Normal"),
    "E-E-C": ("Sleepy", "Normal"),
}


@app.get("/")
def health():
    return {"status": "JUNBELL API running"}


@app.post("/classify")
def classify_alert(alert: JunbellAlert):

    message, alert_level = NOTE_MAP.get(
        alert.note_sequence,
        ("Unknown", "Normal")
    )

    return {
        "patient_name": alert.patient_name,
        "note_sequence": alert.note_sequence,
        "message": message,
        "alert_level": alert_level,
        "sound_type": alert.sound_type,
        "frequency": alert.frequency,
        "intensity": alert.intensity,
        "timestamp": alert.timestamp
    }
@app.get("/")
def health():
    return {"status": "ok"}