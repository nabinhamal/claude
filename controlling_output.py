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

system_message = "You are Nir a helpful assistant.Always be polite and respectful"


stream = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": user_message,
        },
        {"role": "system", "content": system_message},
    ],
    model="llama-3.3-70b-versatile",
    stream=True,
    response_format={"type": "json_object"},
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
    json.loads(chunk.choices[0].delta.content.strip())
print()  # Add a newline
