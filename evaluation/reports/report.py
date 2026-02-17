from evaluation.utils.worst_at_k import worst_at_k, worst_per_gate

def generate_report(results, scores):
    """
    Generates a clinical evaluation report for Mo3een project
    using Qwen 2.5 Free model.

    Parameters:
    - results: list of dicts, each containing 'case_id', 'gate', and individual scores
    - scores: dict with overall 'safety', 'effectiveness', 'hallucination', 'composite' scores
    """
    print("\n===== MOO3EEN EVALUATION REPORT =====\n")

    print(f"Total Cases Evaluated: {len(results)}\n")
    print(f"Overall Safety Score: {scores.get('safety', 0):.3f}")
    print(f"Overall Effectiveness Score: {scores.get('effectiveness', 0):.3f}")
    print(f"Overall Hallucination Score: {scores.get('hallucination', 0):.3f}")
    print(f"Composite Clinical Score: {scores.get('composite', 0):.3f}\n")

    # Worst cases overall
    print("--- Worst Overall Cases ---")
    worst_cases = worst_at_k(results, k=3)
    for r in worst_cases:
        print(f"- Case ID: {r['case_id']}, Gate: {r['gate']}, Score: {r['score']:.2f}")

    # Worst cases per gate (Safety / Effectiveness / Hallucination)
    print("\n--- Worst Cases Per Gate ---")
    worst_by_gate = worst_per_gate(results, k=2)
    for gate, items in worst_by_gate.items():
        print(f"\nGate: {gate}")
        for r in items:
            print(f"  - Case ID: {r['case_id']} -> Score: {r['score']:.2f}")

    print("\n=====================================\n")
    print("Note: Scores reflect Qwen 2.5 Free model performance. Some answers may be generic or imprecise.\n")
