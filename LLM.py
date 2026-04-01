"""
Modern LLM Chatbot — Hugging Face Transformers
CMPG 313 Lab: AI The Past and the Present

Uses Qwen/Qwen2.5-1.5B-Instruct (instruction-tuned, lightweight).
"""

import warnings
warnings.filterwarnings("ignore")

from transformers import pipeline, GenerationConfig

# Load the model once at module level
try:
    chatbot = pipeline(
        "text-generation",
        model="Qwen/Qwen2.5-1.5B-Instruct",
    )
    _model_loaded = True
except Exception as e:
    print(f"[Warning] Could not load LLM: {e}")
    chatbot = None
    _model_loaded = False


def get_llm_response(user_input: str) -> str:
    """Return a response from the instruction-tuned LLM."""
    if not _model_loaded or chatbot is None:
        return "[LLM unavailable — model failed to load.]"

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful, empathetic assistant. "
                "Give clear, concise answers. "
                "Do not repeat the user's words back at the start of your reply."
            ),
        },
        {"role": "user", "content": user_input},
    ]

    gen_config = GenerationConfig(
        max_new_tokens=150,
        do_sample=True,
        temperature=0.7,
    )

    try:
        response = chatbot(
            messages,
            generation_config=gen_config,
        )
        output = response[0]["generated_text"]
        if isinstance(output, list):
            for msg in reversed(output):
                if msg.get("role") == "assistant":
                    return msg["content"].strip()
        return str(output).split("assistant")[-1].strip()

    except Exception as e:
        return f"[Error generating response: {e}]"


# CLI entry point
if __name__ == "__main__":
    print("Modern AI Chatbot (Qwen2.5-1.5B-Instruct)")
    print("Type 'quit' to stop.\n")

    while True:
        user = input("You: ").strip()
        if not user:
            continue
        if user.lower() == "quit":
            print("Bot: Goodbye!")
            break
        print("Bot:", get_llm_response(user), "\n")
