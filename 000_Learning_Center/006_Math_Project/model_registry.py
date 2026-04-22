# model_registry.py

MODEL_REGISTRY = {
    # 🔹 Chat / General Use
    "chat": [
        "llama-3.1-8b-instant",        # fast + cheap
        "llama-3.3-70b-versatile"      # high quality
    ],

    # 🔹 Reasoning / Complex Tasks
    "reasoning": [
        "openai/gpt-oss-120b",         # best reasoning
        "openai/gpt-oss-20b",          # cheaper fallback
        "llama-3.3-70b-versatile"
    ],

    # 🔹 Fast / Low Latency
    "fast": [
        "llama-3.1-8b-instant",
        "openai/gpt-oss-20b"
    ],

    # 🔹 Long Context / RAG
    "long_context": [
        "llama-3.1-8b-instant",
        "openai/gpt-oss-120b"
    ],

    # 🔹 Agent / Tool Use
    "agent": [
        "groq/compound",
        "groq/compound-mini"
    ],

    # 🔹 Vision / Image Tasks (limited support)
    "vision": [
        # depends on availability via API
        # placeholder for future expansion
    ],

    # 🔹 Audio / TTS (Preview - not stable)
    "audio": [
        "canopylabs/orpheus-v1-english",
        "canopylabs/orpheus-arabic-saudi"
    ]
}


def get_models(task: str):
    return MODEL_REGISTRY.get(task, [])


def get_primary_model(task: str):
    models = MODEL_REGISTRY.get(task, [])
    return models[0] if models else None