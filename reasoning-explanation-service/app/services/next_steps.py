from typing import Dict, List
from app.agents.orchestrator import OrchestratorAgent

def generate_next_steps(context: Dict) -> Dict:


    age = context.get("age", 0)
    chronic = context.get("chronic_conditions", [])
    medications = context.get("medications", [])
    symptoms = context.get("symptoms", [])
    labs = context.get("labs", {})

    orchestrator = OrchestratorAgent()

    agent_results = orchestrator.run(
        symptoms=symptoms,
        labs=labs,
        age=age,
        chronic_conditions=chronic,
        medications=medications
    )

    final_explanation = agent_results.get("final_explanation", "")
    steps = [final_explanation] if final_explanation else []

    return {
        "next_steps": steps,
        "agents_output": agent_results
    }
