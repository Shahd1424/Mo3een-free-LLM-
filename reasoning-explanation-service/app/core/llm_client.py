from pathlib import Path
from app.core.guardrails import apply_guardrails

MODEL_PATH = Path(
    "C:/Users/HP/Desktop/healnova-backend-new/models/qwen-2.5b-instruct/qwen2.5-3b-instruct-q4_k_m.gguf"
)


try:
    from gguf import GGUFModel  
except ImportError:
    raise ImportError(
    " pip install gguf-py faild "
    )


class QwenClient:
    def __init__(self, model_path=MODEL_PATH):
        print(f"Loading Qwen model from: {model_path} ...")
        self.model = GGUFModel.load(model_path)
        print("Model loaded successfully ✅")

    def generate(self, prompt: str, max_tokens: int = 512) -> str:
  
        output = self.model.generate(prompt, max_tokens=max_tokens)
        if isinstance(output, list):
            output_str = " ".join([str(o) for o in output])
        else:
            output_str = str(output)

        return apply_guardrails(output_str)


def generate_response(prompt: str, context: dict | None = None) -> str:
    client = QwenClient()
    return client.generate(prompt)


def call_llm(prompt: str) -> str:
    return generate_response(prompt)
