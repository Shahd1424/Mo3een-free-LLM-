from fastapi import APIRouter, HTTPException
from app.schemas.models import (
    FullReasoningRequest, FullReasoningResponse,
    SymptomReasoningRequest, SymptomReasoningResponse,
    LabExplanationRequest, LabExplanationResponse,
    NextStepsRequest, NextStepsResponse,
)
from app.utils.logger import get_logger, generate_request_id
from app.core.llm_client import QwenClient 

from app.services.symptom_reasoning import reason_about_symptoms
from app.services.lab_explanation import explain_labs
from app.services.next_steps import generate_next_steps

router = APIRouter()
logger = get_logger("reasoning-api")
llm_client = QwenClient()  

# ---------------- Symptoms ----------------
@router.post("/reasoning/symptoms", response_model=SymptomReasoningResponse)
def symptoms_reasoning(payload: SymptomReasoningRequest):
    req_id = generate_request_id()
    logger.info(f"[{req_id}] Symptoms reasoning request")

    try:
        result = reason_about_symptoms(
            payload.symptoms,
            payload.context.dict() if payload.context else {},
            llm_client=llm_client
        )

        return {
            "explanation": result["explanation"],
            "severity_hint": result.get("severity_hint"),
            "disclaimer": "This is not a medical diagnosis."
        }

    except Exception as e:
        logger.error(f"[{req_id}] Error: {e}")
        raise HTTPException(status_code=500, detail="Internal reasoning error")


# ---------------- Labs ----------------
@router.post("/reasoning/labs", response_model=LabExplanationResponse)
def lab_reasoning(payload: LabExplanationRequest):
    req_id = generate_request_id()

    try:
        explanation = explain_labs(
            payload.labs,
            payload.context.dict() if payload.context else {},
            llm_client=llm_client
        )

        return {
            "explanation": explanation,
            "disclaimer": "Lab explanations are informational only."
        }

    except Exception as e:
        logger.error(f"[{req_id}] Error: {e}")
        raise HTTPException(status_code=500, detail="Lab explanation failed")


# ---------------- Next Steps ----------------
@router.post("/reasoning/next-steps", response_model=NextStepsResponse)
def next_steps(payload: NextStepsRequest):
    try:
        steps = generate_next_steps(payload.context, llm_client=llm_client)
        return {
            "steps": steps,
            "disclaimer": "No prescriptions or emergency actions included."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Next steps generation failed")


# ---------------- Full Reasoning ----------------
@router.post("/reasoning/full", response_model=FullReasoningResponse)
def full_reasoning(payload: FullReasoningRequest):
    req_id = generate_request_id()
    logger.info(f"[{req_id}] Full reasoning request")

    try:
        context = payload.context.model_dump() if payload.context else {}

        symptoms_result = reason_about_symptoms(payload.symptoms, context, llm_client=llm_client)
        labs_result = explain_labs(payload.labs, context, llm_client=llm_client)
        next_steps_result = generate_next_steps(context, llm_client=llm_client)

        return {
            "symptoms_explanation": (
                symptoms_result["explanation"]
                if isinstance(symptoms_result, dict)
                else symptoms_result
            ),
            "labs_explanation": (
                labs_result["explanation"]
                if isinstance(labs_result, dict)
                else labs_result
            ),
            "next_steps": (
                "\n".join(next_steps_result["next_steps"])
                if isinstance(next_steps_result, dict)
                else (
                    "\n".join(next_steps_result)
                    if isinstance(next_steps_result, list)
                    else next_steps_result
                )
            ),
            "disclaimer": "This is not a medical diagnosis."
        }

    except Exception as e:
        logger.error(f"[{req_id}] Error: {e}")
        raise HTTPException(status_code=500, detail="Full reasoning failed")
