import json
from pathlib import Path

from evaluation.runners.run_single_case import run_case
from evaluation.utils.scoring import aggregate_scores
from evaluation.reports.report import generate_report

def run_all_cases():
    """
    Run evaluation on all clinical/educational cases for Mo3een project.
    Uses Qwen 2.5 Free model to generate explanations and evaluates:
    - Safety
    - Effectiveness
    - Hallucination
    """
    # Path to the JSON file containing test cases
    cases_path = Path("evaluation/cases/symptom_reasoning.json")

    if not cases_path.exists():
        print(f"Cases file not found: {cases_path}")
        return []

    with open(cases_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    results = []

    for case in cases:
        print(f"\n===== Running case: {case['case_id']} =====")
        try:
            # Run the case through the evaluation pipeline
            result = run_case(case)
            results.append(result)

            # Print a brief summary for UI-like output
            print(f"Case ID: {case['case_id']}")
            print(f"  Safety Score: {result.get('safety_score', 0):.2f}")
            print(f"  Effectiveness Score: {result.get('effectiveness_score', 0):.2f}")
            print(f"  Hallucination Score: {result.get('hallucination_score', 0):.2f}")
            print(f"  Composite Score: {result.get('composite_score', 0):.2f}")

        except Exception as e:
            print(f"Error evaluating case {case['case_id']}: {e}")

    return results

if __name__ == "__main__":
    # Run all cases
    results = run_all_cases()

    if not results:
        print("No results to report.")
    else:
        # Aggregate overall scores
        scores = aggregate_scores(results)

        # Generate the final report
        generate_report(results, scores)
