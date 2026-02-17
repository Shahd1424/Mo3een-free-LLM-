def worst_at_k(results, k=3):
    """
    Returns the k worst scoring cases overall.
    """
    sorted_results = sorted(results, key=lambda x: x["score"])
    return sorted_results[:k]


def worst_per_gate(results, k=2):
    """
    Returns worst k cases per gate.
    """
    gates = {}
    for r in results:
        gates.setdefault(r["gate"], []).append(r)

    worst = {}
    for gate, items in gates.items():
        sorted_items = sorted(items, key=lambda x: x["score"])
        worst[gate] = sorted_items[:k]

    return worst
