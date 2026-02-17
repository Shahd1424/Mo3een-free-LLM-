from app.agents.triage_agent import TriageAgent
from app.agents.emergency_agent import EmergencyAgent
from app.agents.medication_agent import MedicationSafetyAgent
from app.agents.caregiver_agent import CaregiverNotificationAgent
from app.core.llm_client import QwenClient

class OrchestratorAgent:
    def __init__(self):
        llm_client = QwenClient() 
        self.triage = TriageAgent(llm_client)
        self.emergency = EmergencyAgent()
        self.medication = MedicationSafetyAgent(llm_client)
        self.caregiver = CaregiverNotificationAgent()

def run(self, symptoms, labs, age, chronic_conditions, medications):

    # Emergency check
    emergency_result = self.emergency.evaluate(symptoms)

    # Triage evaluation
    triage_result = self.triage.evaluate(
        symptoms=symptoms,
        labs=labs,
        age=age,
        chronic_conditions=chronic_conditions
    )

    #  Medication safety
    medication_result = self.medication.evaluate(
        medications=medications,
        labs=labs,
        age=age
    )

    #  Caregiver decision
    urgency_level = "low"
    try:
        import json
        triage_json = json.loads(triage_result)
        urgency_level = triage_json.get("urgency", "low")
    except:
        pass

    lab_abnormal = any(isinstance(v, (int, float)) and v > 1.5 for v in labs.values())
    
    caregiver_result = self.caregiver.evaluate(
        urgency_level=urgency_level,
        emergency_flag=emergency_result["emergency"],
        lab_abnormal=lab_abnormal
    )

    # Final explanation
    final_prompt = f"""
You are a senior clinical reasoning assistant.
Patient Data:
Emergency: {emergency_result}
Triage: {triage_result}
Medication Safety: {medication_result}
"""
    if emergency_result.get("emergency"):
        final_explanation = """
Red flag symptoms detected (e.g., chest pain, shortness of breath).
Seek emergency medical care immediately.
"""
    else:
        final_explanation = llm_client.generate(final_prompt)

    return {
        "emergency": emergency_result,
        "triage": triage_result,
        "medication_safety": medication_result,
        "caregiver_decision": caregiver_result,
        "final_explanation": final_explanation
    }
