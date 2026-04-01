"""
ELIZA-style Chatbot — Custom Rule-Based Version
CMPG 313 Lab: AI The Past and the Present

Custom modifications:
  1. Added greeting/name patterns (Hello, My name is...)
  2. Added stress/exam-related responses
  3. Added family-related responses (mother, father, parents)
  4. Added sleep/fatigue responses
  5. Added need/want responses
  6. Added "because" follow-up handling
  7. Added fallback/default responses
"""

import re
import random

# ─────────────────────────────────────────────
# Rule set: list of (pattern, [responses])
# Patterns are matched case-insensitively.
# ─────────────────────────────────────────────
RULES = [
    # 1. Greetings
    (r"hello|hi|hey",
     [
         "Hello! How are you feeling today?",
         "Hi there. What's on your mind?",
         "Hey! What would you like to talk about?",
     ]),

    # 2. Name introduction
    (r"my name is (.+)",
     [
         "Hello, {0}. Why have you come to me today?",
         "Nice to meet you, {0}. What's troubling you?",
         "So, {0} — tell me more about yourself.",
     ]),

    # 3. Stress / anxiety
    (r"i (feel|am) (stressed|anxious|worried|nervous)",
     [
         "Why do you feel {1}?",
         "How long have you been feeling {1}?",
         "What do you think is making you feel {1}?",
         "Does feeling {1} happen often for you?",
     ]),

    # 4. Exams / school
    (r"(exam|exams|test|tests|school|university|studies)",
     [
         "How are your studies affecting you?",
         "Do you feel prepared for your exams?",
         "Is academic pressure something you deal with often?",
         "Tell me more about how your studies make you feel.",
     ]),

    # 5. Tiredness / sleep
    (r"i (am|feel) (tired|exhausted|sleepy|drained)",
     [
         "Why do you think you are feeling {1}?",
         "How much sleep have you been getting?",
         "Does being {1} affect your daily life?",
         "What do you do when you feel {1}?",
     ]),

    # 6. Need / want
    (r"i need (.+)",
     [
         "Why do you need {0}?",
         "Would getting {0} really help you?",
         "What would change if you had {0}?",
     ]),

    (r"i want (.+)",
     [
         "What would it mean to you to have {0}?",
         "Why do you want {0}?",
         "If you had {0}, how would things be different?",
     ]),

    # 7. Family — mother
    (r"my mother|my mom",
     [
         "Tell me more about your relationship with your mother.",
         "How does your mother make you feel?",
         "What has your mother said or done recently?",
     ]),

    # 8. Family — father
    (r"my father|my dad",
     [
         "How do you get along with your father?",
         "What kind of relationship do you have with your father?",
         "Does your father's behaviour affect you?",
     ]),

    # 9. Family — general
    (r"my (family|parents|siblings|brother|sister)",
     [
         "Tell me more about your {0}.",
         "How does your {0} influence how you feel?",
         "Are things at home with your {0} going well?",
     ]),

    # 10. "Because" follow-up
    (r"because (.+)",
     [
         "Is that the real reason?",
         "Does that reason fully explain how you feel?",
         "What else might be contributing?",
         "How long has {0} been a factor?",
     ]),

    # 11. "I am" general
    (r"i am (.+)",
     [
         "How long have you been {0}?",
         "What made you {0}?",
         "Does being {0} bother you?",
         "How does being {0} make you feel?",
     ]),

    # 12. "I feel" general
    (r"i feel (.+)",
     [
         "Why do you feel {0}?",
         "Do you often feel {0}?",
         "What triggers the feeling of {0}?",
     ]),

    # 13. Yes / No
    (r"^yes$|^yeah$|^yep$",
     [
         "You seem quite sure. Can you elaborate?",
         "Why is that?",
         "I see. Tell me more.",
     ]),

    (r"^no$|^nope$",
     [
         "Why not?",
         "Are you certain about that?",
         "Can you explain?",
     ]),

    # 14. Quit
    (r"quit|bye|goodbye|exit",
     ["Goodbye. Take care of yourself.", "Farewell. Come back anytime."]),
]


def get_eliza_response(user_input: str) -> str:
    """Return a rule-based ELIZA response for the given user input."""
    text = user_input.strip()

    for pattern, responses in RULES:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            reply = random.choice(responses)
            # Fill in captured groups if the response template uses {0}, {1}, …
            try:
                groups = match.groups()
                reply = reply.format(*groups)
            except (IndexError, KeyError):
                pass
            return reply

    # Default / fallback responses
    defaults = [
        "Can you tell me more?",
        "I see. Go on.",
        "Why do you say that?",
        "That's interesting. Please continue.",
        "How does that make you feel?",
        "And what do you think about that?",
    ]
    return random.choice(defaults)


# ─────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("ELIZA Chatbot (Custom Rule-Based)")
    print("Type 'quit' to stop.\n")

    while True:
        user = input("You: ").strip()
        if not user:
            continue
        response = get_eliza_response(user)
        print(f"ELIZA: {response}\n")
        if re.search(r"quit|bye|goodbye|exit", user, re.IGNORECASE):
            break
