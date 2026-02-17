from pydantic import BaseModel, Field
from typing import List, Dict, Optional


# -------- Shared --------
class PatientContext(BaseModel):
    age: Optional[int] = Field(None, ge=0)
    gender: Optional[str] = None
    chronic_conditions: Optional[List[str]] = Field(default_factory=list)

# -------- Symptoms --------

class SymptomReasoningRequest(BaseModel):
    symptoms: list[str] = Field(..., min_length=1)
    context: Optional[PatientContext] = None



class SymptomReasoningResponse(BaseModel):
    explanation: str
    severity_hint: Optional[str] = None
    disclaimer: str


# -------- Labs --------
class LabExplanationRequest(BaseModel):
    labs: Dict[str, float]
    context: Optional[PatientContext] = None


class LabExplanationResponse(BaseModel):
    explanation: str
    disclaimer: str


# -------- Next Steps --------
class NextStepsRequest(BaseModel):
    context: Dict


class NextStepsResponse(BaseModel):
    steps: str
    disclaimer: str
class FullReasoningRequest(BaseModel):
    symptoms: list[str]
    labs: dict[str, float]
    context: Optional[PatientContext] = None

class FullReasoningResponse(BaseModel):
    symptoms_explanation: str
    labs_explanation: str
    next_steps: str
    disclaimer: str
