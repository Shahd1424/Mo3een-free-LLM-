from evaluation.judges.safety_judge import SafetyJudge
from evaluation.judges.effectiveness_judge import EffectivenessJudge
from evaluation.judges.hallucination_judge import HallucinationJudge
from app.services.symptom_reasoning import reason_about_symptoms

def run_case(case):
    """
    Run a single case through Mo3een evaluation pipeline:
    - Safety
    - Effectiveness
    - Hallucination
    Uses Qwen 2.5 Free model for generating explanations.
    """

    input_data = case.get("input", {})
    gate = case.get("gate", "")

    # Generate model response
    try:
        response = reason_about_symptoms(
            symptoms=input_data.get("symptoms", []),
            patient_context={
                "age": input_data.get("age", 0),
                "chronic_conditions": input_data.get("chronic_conditions", [])
            }
        )
    except Exception as e:
        print(f"Error generating model response for case {case.get('case_id')}: {e}")
        return {
            "case_id": case.get("case_id", "unknown"),
            "gate": gate,
            "risk_weight": case.get("risk_weight", 1),
            "judge_output": {},
            "score": 0
        }

    model_text = response.get("explanation", "")

    # Debug printing like UI
    print(f"\n===== Case: {case.get('case_id')} | Gate: {gate} =====")
    print("Model Response:")
    print(model_text)
    print("================================")

    judge_output = {}
    score = 0

    # Evaluate based on gate
    if gate == "safety":
        judge = SafetyJudge()
        judge_output = judge.score(case, model_text)
        score = 1 - max(
            judge_output.get("contraindication", 1),
            judge_output.get("missed_critical", 1)
        )

    elif gate == "effectiveness":
        judge = EffectivenessJudge()
        judge_output = judge.score(case, model_text)
        score = (
            judge_output.get("diagnostic_accuracy", 0) +
            judge_output.get("clinical_reasoning", 0) +
            judge_output.get("explanation_quality", 0)
        ) / 3

    elif gate == "hallucination":
        judge = HallucinationJudge()
        judge_output = judge.score(case, model_text)
        score = judge_output.get("score", 0)

    else:
        print(f"Unknown gate: {gate} for case {case.get('case_id')}")

    return {
        "case_id": case.get("case_id", "unknown"),
        "gate": gate,
        "risk_weight": case.get("risk_weight", 1),
        "judge_output": judge_output,
        "score": score
    }
