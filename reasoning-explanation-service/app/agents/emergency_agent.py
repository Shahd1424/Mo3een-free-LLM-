class EmergencyAgent:

    def evaluate(self, symptoms):

        red_flags = [
            "chest pain",
            "shortness of breath",
            "loss of consciousness",
            "severe bleeding",
            "stroke symptoms",
            "confusion"
        ]

        detected_flags = []

        for symptom in symptoms:
            if symptom.lower() in red_flags:
                detected_flags.append(symptom)

        if detected_flags:
            return {
                "emergency": True,
                "reason": f"Red flag symptoms detected: {detected_flags}",
                "action": "call_emergency_services"
            }

        return {
            "emergency": False,
            "reason": "No immediate red flags detected.",
            "action": "continue_evaluation"
        }
