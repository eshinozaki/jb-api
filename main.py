from fastapi import FastAPI
from pydantic import BaseModel
from collections import defaultdict, Counter
import re

app = FastAPI(title="JUNBELL AI Learning Server")

# In-memory AI learning store
# memory[patient_name][normalized_question] = Counter({"TIRED": 3, "PAIN": 1})
memory = defaultdict(lambda: defaultdict(Counter))


def normalize_question(question: str) -> str:
    question = question.lower().strip()
    question = re.sub(r"[^\w\s]", "", question)
    question = re.sub(r"\s+", " ", question)
    return question


# Starter training dictionary (50 questions)
training_dictionary = {
    "how are you feeling today": ["I'M OKAY", "TIRED", "PAIN"],
    "are you feeling okay right now": ["YES", "NO", "TIRED"],
    "do you feel better than yesterday": ["YES", "NO", "I'M OKAY"],
    "are you comfortable right now": ["YES", "NO", "PAIN"],
    "are you feeling tired": ["TIRED", "YES", "NO"],
    "do you feel weak today": ["YES", "NO", "TIRED"],
    "are you feeling stronger today": ["YES", "NO", "I'M OKAY"],
    "are you feeling normal today": ["YES", "NO", "I'M OKAY"],

    "are you feeling any pain": ["PAIN", "YES", "NO"],
    "is the pain getting worse": ["YES", "NO", "PAIN"],
    "is the pain getting better": ["YES", "NO", "I'M OKAY"],
    "does your head hurt": ["PAIN", "YES", "NO"],
    "does your chest hurt": ["PAIN", "YES", "NO"],
    "does your arm hurt": ["PAIN", "YES", "NO"],
    "does your leg hurt": ["PAIN", "YES", "NO"],
    "do you feel pressure in your chest": ["PAIN", "YES", "NO"],
    "do you feel discomfort anywhere": ["PAIN", "YES", "NO"],

    "are you having trouble breathing": ["YES", "NO", "TIRED"],
    "do you feel short of breath": ["YES", "NO", "TIRED"],
    "does your heart feel like it is beating fast": ["YES", "NO", "TIRED"],
    "do you feel dizzy": ["YES", "NO", "TIRED"],
    "do you feel lightheaded": ["YES", "NO", "TIRED"],
    "do you feel your heart pounding": ["YES", "NO", "TIRED"],
    "do you feel chest tightness": ["PAIN", "YES", "NO"],

    "are you thirsty": ["WATER", "YES", "NO"],
    "do you want water": ["WATER", "YES", "NO"],
    "are you hungry": ["FOOD", "YES", "NO"],
    "do you want food": ["FOOD", "YES", "NO"],
    "do you need to go to the bathroom": ["BATHROOM", "YES", "NO"],
    "do you need help moving": ["YES", "NO", "TIRED"],
    "do you want to change position": ["YES", "NO", "TIRED"],
    "do you want a blanket": ["YES", "NO", "TIRED"],

    "can you move your hand comfortably": ["YES", "NO", "TIRED"],
    "is your arm weaker today": ["YES", "NO", "TIRED"],
    "can you move your leg easily": ["YES", "NO", "TIRED"],
    "do you feel numbness anywhere": ["YES", "NO", "TIRED"],
    "is your vision blurry today": ["YES", "NO", "TIRED"],
    "do you feel tingling anywhere": ["YES", "NO", "TIRED"],

    "do you understand what i am saying": ["YES", "NO", "I'M OKAY"],
    "do you recognize me": ["YES", "NO", "I'M OKAY"],
    "do you know where you are right now": ["YES", "NO", "I'M OKAY"],

    "are you feeling sad today": ["YES", "NO", "TIRED"],
    "are you feeling worried right now": ["YES", "NO", "TIRED"],
    "are you feeling happy today": ["YES", "NO", "I'M OKAY"],
    "do you feel frustrated right now": ["YES", "NO", "TIRED"],

    "did you sleep well last night": ["YES", "NO", "TIRED"],
    "are you feeling sleepy right now": ["SLEEPY", "YES", "NO"],
    "do you want your medicine now": ["MEDICINE", "YES", "NO"],
    "do you feel better after your medicine": ["YES", "NO", "I'M OKAY"],
    "do you want to rest": ["TIRED", "YES", "NO"],

    "do you feel nauseous": ["YES", "NO", "TIRED"],
    "do you want to see your family": ["YES", "NO", "HAPPY"],
}


class PredictRequest(BaseModel):
    patient_name: str
    doctor_question: str


class LearnRequest(BaseModel):
    patient_name: str
    doctor_question: str
    actual_response: str


class ClassifyRequest(BaseModel):
    timestamp: str
    patient_name: str
    message: str
    alert_level: str
    frequency: str
    intensity: str
    notes_detected: str


@app.get("/")
def health():
    return {"status": "JUNBELL AI Learning Server running"}


@app.post("/predict-response")
def predict_response(data: PredictRequest):
    patient = data.patient_name.upper().strip()
    normalized = normalize_question(data.doctor_question)

    learned = memory[patient].get(normalized)

    if learned and len(learned) > 0:
        most_common = learned.most_common(3)
        suggestions = [item[0] for item in most_common]
        total = sum(learned.values())
        top_count = most_common[0][1]
        confidence = round(top_count / total, 2) if total else 0.0

        return {
            "seen_before": True,
            "normalized_question": normalized,
            "suggestions": suggestions,
            "confidence": confidence
        }

    fallback = training_dictionary.get(normalized, ["I'M OKAY", "TIRED", "PAIN"])

    return {
        "seen_before": False,
        "normalized_question": normalized,
        "suggestions": fallback[:3],
        "confidence": 0.0
    }


@app.post("/learn-response")
def learn_response(data: LearnRequest):
    patient = data.patient_name.upper().strip()
    normalized = normalize_question(data.doctor_question)
    response = data.actual_response.upper().strip()

    memory[patient][normalized][response] += 1
    learned = memory[patient][normalized]

    return {
        "status": "learned",
        "patient_name": patient,
        "normalized_question": normalized,
        "response_counts": dict(learned)
    }


@app.post("/classify")
def classify_alert(alert: ClassifyRequest):
    return {
        "timestamp": alert.timestamp,
        "patient_name": alert.patient_name,
        "message": alert.message,
        "alert_level": alert.alert_level,
        "frequency": alert.frequency,
        "intensity": alert.intensity,
        "notes_detected": alert.notes_detected
    }
