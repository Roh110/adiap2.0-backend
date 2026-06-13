from agents.gemini_helper import ask_gemini

response = ask_gemini(
    "Explain bearing wear in a CNC machine in 50 words."
)

print(response)