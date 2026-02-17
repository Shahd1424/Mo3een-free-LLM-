class CaregiverNotificationAgent:

    def evaluate(self, urgency_level, emergency_flag, lab_abnormal):

        if emergency_flag:
            return {
                "notify": True,
                "reason": "Emergency condition detected.",
                "action": "alert_caregiver_immediately"
            }

        if urgency_level == "high":
            return {
                "notify": True,
                "reason": "High urgency condition.",
                "action": "notify_caregiver"
            }

        if lab_abnormal:
            return {
                "notify": True,
                "reason": "Abnormal lab values detected.",
                "action": "notify_caregiver"
            }

        return {
            "notify": False,
            "reason": "No caregiver notification needed.",
            "action": "none"
        }
