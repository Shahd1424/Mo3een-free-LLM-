from typing import List, Dict
from app.agents.orchestrator import OrchestratorAgent

HIGH_RISK_SYMPTOMS = {
    "chest pain",
    "shortness of breath",
    "confusion",
    "loss of consciousness",
    "sudden weakness",
    "palpitations"
}


def assess_severity(symptoms: List[str], age: int) -> str:
    for s in symptoms:
        if s.lower() in HIGH_RISK_SYMPTOMS:
            return "high"

    if age >= 65 and len(symptoms) >= 3:
        return "moderate"

    return "low"


def detect_conflicts(symptoms: List[str]) -> List[str]:
    conflicts = []
    lowered = [s.lower() for s in symptoms]

    if "fever" in lowered and "low body temperature" in lowered:
        conflicts.append("Conflicting temperature signals")

    if "weight loss" in lowered and "weight gain" in lowered:
        conflicts.append("Conflicting weight changes")

    return conflicts


def reason_about_symptoms(symptoms: List[str], patient_context: Dict) -> Dict:
    age = patient_context.get("age", 0)
    chronic = patient_context.get("chronic_conditions", [])

    severity = assess_severity(symptoms, age)
    conflicts = detect_conflicts(symptoms)

    orchestrator = OrchestratorAgent()

    labs = patient_context.get("labs", {})
    medications = patient_context.get("medications", [])

    agent_results = orchestrator.run(
        symptoms=symptoms,
        labs=labs,
        age=age,
        chronic_conditions=chronic,
        medications=medications
    )

    return {
        "severity_hint": severity,
        "conflicts": conflicts,
        "explanation": agent_results.get("final_explanation"),
        "agents_output": agent_results
    }
