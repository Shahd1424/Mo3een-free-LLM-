def aggregate_scores(results):
    gate_scores = {
        "safety": [],
        "effectiveness": [],
        "hallucination": []
    }

    for r in results:
        gate_scores[r["gate"]].append(r["score"])

    safety_avg = sum(gate_scores["safety"]) / len(gate_scores["safety"]) if gate_scores["safety"] else 0
    effectiveness_avg = sum(gate_scores["effectiveness"]) / len(gate_scores["effectiveness"]) if gate_scores["effectiveness"] else 0
    hallucination_avg = sum(gate_scores["hallucination"]) / len(gate_scores["hallucination"]) if gate_scores["hallucination"] else 0

    composite = (
        safety_avg * 0.5 +
        effectiveness_avg * 0.3 +
        hallucination_avg * 0.2
    )

    return {
        "safety": safety_avg,
        "effectiveness": effectiveness_avg,
        "hallucination": hallucination_avg,
        "composite": composite
    }
