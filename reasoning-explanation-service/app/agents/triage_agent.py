
from app.core.llm_client import QwenClient

class TriageAgent:
    def __init__(self, llm_client: QwenClient = None):
        self.llm_client = llm_client or QwenClient()

    def evaluate(self, symptoms, labs, age, chronic_conditions):
        prompt = f"""
You are a clinical triage assistant.

Patient information:
- Age: {age}
- Symptoms: {symptoms}
- Labs: {labs}
- Chronic conditions: {chronic_conditions}

Provide:
- Urgency level (low/medium/high)
- Recommended immediate actions
- Structured JSON output
"""
        response = self.llm_client.generate(prompt)
        return response


class MedicationSafetyAgent:
    def __init__(self, llm_client: QwenClient = None):
        self.llm_client = llm_client or QwenClient()

    def evaluate(self, medications, labs, age):
        prompt = f"""
You are a medication safety assistant.

Patient information:
- Age: {age}
- Current medications: {medications}
- Lab results: {labs}

Your tasks:
1. Detect potential drug-drug interactions.
2. Detect unsafe use in kidney or liver impairment.
3. Detect unsafe combinations.
4. DO NOT prescribe new medications.

Return JSON only:
{{
  "interaction_risk": "...",
  "organ_risk": "...",
  "overall_safety": "safe / caution / unsafe",
  "reason": "..."
}}
"""
        response = self.llm_client.generate(prompt)
        return response
