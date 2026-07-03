from pydantic import BaseModel
from typing import Optional, Dict

class PredictionInput(BaseModel):
    age: int
    bmi: float
    heart_rate: int
    glucose: float
    steps: int
    sleep_hours: float
    gender: Optional[str] = "male"
    blood_pressure: Optional[str] = "120/80"

class Token(BaseModel):
    access_token: str
    token_type: str

class ChatInput(BaseModel):
    query: str
