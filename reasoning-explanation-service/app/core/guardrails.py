DISALLOWED_PATTERNS = [
    "you have .* disease",
    "you should take .*",
    "prescribe",
    "medication",
    "emergency",
]

DISCLAIMER = (
    "⚠️ This information is for educational purposes only "
    "and does not replace professional medical advice."
)

def is_unsafe(text: str) -> bool:
    lower = text.lower()
    return any(p in lower for p in [
        "you have",
        "take this medication",
        "diagnosis",
        "emergency immediately"
    ])

def apply_guardrails(text: str) -> str:
    if is_unsafe(text):
        return (
            f"{DISCLAIMER}\n\n"
            "I can share general educational information, "
            "but I can’t provide medical decisions or instructions."
        )

    return f"{DISCLAIMER}\n\n{text}"
