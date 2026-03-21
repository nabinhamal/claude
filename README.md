# AI Development Cheat Sheet: Claude & Groq API

This project documents patterns and lessons for building with Claude/Groq APIs. Use this as a reference for future development.

## 🚀 1. Setup & Initialization

```python
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
model = "llama-3.3-70b-versatile" # Or claude-3-5-sonnet-latest
```

## 💬 2. Message Structure
Always use roles to define behavior and context:
- **System**: Defines the persona and global rules.
- **User**: The specific task or question.
- **Assistant**: Use for "pre-filling" (bootstrapping) consistent outputs.

```python
messages = [
    {"role": "system", "content": "You are a specialized AWS architect."},
    {"role": "user", "content": "Generate an S3 policy for read-only access."},
    {"role": "assistant", "content": "```json"} # Pre-filling for JSON
]
```

## 🛠️ 3. Generic Chat Helper
A robust helper for handling API calls with system prompts and stop sequences.

```python
def chat(messages, system=None, temperature=1.0, stop_sequences=[]):
    if system:
        messages = [{"role": "system", "content": system}] + messages
        
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        stop=stop_sequences if stop_sequences else None,
    )
    return response.choices[0].message.content
```

## 📊 4. Prompt Evaluation Workflow
To iterate on prompts, follow this three-step "Grader" workflow:

1.  **Generate Dataset**: Use the LLM to generate a `dataset.json` with `task` and `expected_output`.
2.  **Execute Prompts**: Loop through the dataset and call your target prompt logic.
3.  **Model Grading**: Pass the `task` + `actual_output` back to an "expert" LLM to assign a 1-10 score and reasoning.

```python
def run_eval(dataset):
    results = []
    for test_case in dataset:
        output = run_prompt(test_case)
        grade = grade_by_model(test_case, output)
        results.append({"case": test_case, "score": grade['score']})
    return results
```

## 🎯 5. Controlling Output
- **JSON Mode**: Use a system prompt like "Always respond with valid JSON" and pre-fill the assistant message with `{` or ` ```json `.
- **Stop Sequences**: Use `stop=["```"]` (API parameter is `stop`, but typically called stop sequences).

## 🌡️ 6. Temperature Selection Guide
The `temperature` parameter controls the "randomness" of the model's output. Choose based on your task:

| Task Type | Recommended Temp | Reasoning |
| :--- | :--- | :--- |
| **Grading & Evaluation** | `0.0` | Ensures consistent, objective scoring. |
| **Data Extraction / JSON** | `0.0` | Minimizes formatting errors and ensures field accuracy. |
| **Summarization** | `0.3 - 0.5` | Keeps the model focused while allowing for natural flow. |
| **Code Generation** | `0.2 - 0.7` | Balanced for creative but syntactically correct code. |
| **Creative Writing** | `0.8 - 1.0` | Encourages diverse vocabulary and variability. |
| **Brainstorming** | `1.0+` | Maximizes the breadth of ideas. |

> [!TIP]
> Use `0.0` for any task where consistency is more important than creativity (e.g., automated testing).

## 🔐 7. PASETO (Platform-Agnostic Security Tokens)
PASETO is a more secure alternative to JWT. Use it for session tokens or cross-service authentication.

Refer to [paseto_guide.py](file:///Users/d3vil/Documents/projects/ac/auth/paseto_guide.py) for full implementation details.

### Quick Example (Symmetric)
```python
from pyseto import Key, Pyseto
import os

key = Key.new(version=4, purpose="local", key=os.urandom(32))
token = Pyseto.encode(key, {"user": "nabin", "role": "admin"})
# Decoded: Pyseto.decode(key, token)
```

> [!IMPORTANT]
> Always use `v4` and `purpose="local"` for internal tokens. Use `purpose="public"` for asymmetric signatures.

### JS Example (Node.js)
Refer to [paseto_guide.js](file:///Users/d3vil/Documents/projects/ac/auth/paseto_guide.js) for details.

```javascript
const { V4 } = require('paseto');
const token = await V4.encrypt({ user: 'nabin' }, secretKey);
// const payload = await V4.decrypt(token, secretKey);
```
