from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import joblib
import numpy as np
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = os.path.join(os.path.dirname(__file__), '../model/model.pkl')
model = joblib.load(model_path)

class Lead(BaseModel):
    email: EmailStr
    credit_score: int
    age_group: str
    family: str
    income: int
    comments: str
    consent: bool

def encode_inputs(age_group, family):
    age_map = {'18-25': 0, '26-35': 1, '36-50': 2, '51+': 3}
    fam_map = {'Single': 0, 'Married': 1, 'Married with Kids': 2}
    return age_map[age_group], fam_map[family]

def rerank(score, comment):
    comment = comment.lower()
    adjust = 0
    if 'urgent' in comment: adjust += 10
    if 'soon' in comment: adjust += 15
    if 'not interested' in comment: adjust -= 10
    if 'relocation' in comment: adjust += 10
    return max(0, min(100, score + adjust))

@app.post("/score")
def score_lead(lead: Lead):
    if not lead.consent:
        return {"error": "Consent not given"}

    age_code, fam_code = encode_inputs(lead.age_group, lead.family)
    features = np.array([[lead.credit_score, age_code, fam_code, lead.income]])
    score = model.predict_proba(features)[0][1] * 100
    reranked = rerank(score, lead.comments)

    return {
        "email": lead.email,
        "initial_score": round(score, 2),
        "reranked_score": round(reranked, 2),
        "comments": lead.comments
    }