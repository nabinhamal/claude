import os
from dotenv import load_dotenv
from groq import Groq
import json

# Load environment variables from .env
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Get input from the user
user_message = input("You: ")

stream = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": user_message,
        },
        {
            "role": "system",
            "content": "You are Nir a helpful assistant.",
        },
    ],
    model="llama-3.3-70b-versatile",
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
print()  # Add a newline at the end
