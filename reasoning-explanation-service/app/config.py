from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ----------------------------
    # Local LLM Configuration
    # ----------------------------

    MODEL_PATH: str = "models/qwen2.5-3b-instruct-q4_k_m.gguf"
    MODEL_CONTEXT_SIZE: int = 2048      # max context length
    MODEL_N_THREADS: int = 6            # suitable for your CPU
    MODEL_TEMPERATURE: float = 0.3
    MODEL_TOP_P: float = 0.9
    MODEL_MAX_TOKENS: int = 400

    # ----------------------------
    # App Configuration
    # ----------------------------

    TIMEOUT: int = 25

    SYSTEM_PROMPT: str = (
        "You are an explanation assistant. Provide simplified and clear explanations. "
        "Avoid giving medical diagnoses or prescriptions. "
        "Keep your answers concise and helpful."
    )

    class Config:
        env_file = ".env"


settings = Settings()


