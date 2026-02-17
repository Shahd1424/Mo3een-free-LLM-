
from typing import Dict
from app.agents.orchestrator import OrchestratorAgent

REFERENCE_RANGES = {
    "hemoglobin": "Usually around 12–17 g/dL",
    "cholesterol": "Total cholesterol often below 200 mg/dL",
    "glucose": "Fasting levels often around 70–100 mg/dL"
}

def explain_labs(labs: Dict[str, float], patient_context: Dict) -> Dict:
  

    age = patient_context.get("age", 0)
    chronic = patient_context.get("chronic_conditions", [])
    medications = patient_context.get("medications", [])
    symptoms = patient_context.get("symptoms", [])

    orchestrator = OrchestratorAgent()

    agent_results = orchestrator.run(
        symptoms=symptoms,
        labs=labs,
        age=age,
        chronic_conditions=chronic,
        medications=medications
    )

    return {
        "labs": labs,
        "explanation": agent_results.get("final_explanation"),
        "agents_output": agent_results
    }
