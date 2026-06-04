import re

def security_check(user_input):

    blocked_words = [
        "ignore previous instructions",
        "system prompt",
        "hack",
        "exploit",
        "bypass"
    ]

    text = user_input.lower()

    for word in blocked_words:

        if word in text:

            return {
                "safe": False,
                "message": "Unsafe input detected"
            }

    cleaned = re.sub(r"[<>]", "", user_input)

    return {
        "safe": True,
        "clean_text": cleaned
    }