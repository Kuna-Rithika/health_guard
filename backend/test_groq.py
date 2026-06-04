from .groq_service import ask_groq

result = ask_groq(
    "You are a helpful doctor.",
    "I have fever and headache."
)

print(result)