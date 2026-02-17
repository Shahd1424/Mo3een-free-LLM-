from app.core.llm_client import QwenClient

class MedicationSafetyAgent:
    def __init__(self, llm_client: QwenClient):
        self.llm_client = llm_client

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
