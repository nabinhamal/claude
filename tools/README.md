# Tool Use with Claude (Anthropic API)

This guide explains how to implement and use tools (function calling) with Anthropic's Claude models. Tool use allows Claude to interact with external tools and APIs, enabling more complex workflows.

## Prerequisites

- `anthropic` Python SDK installed: `pip install anthropic`
- Anthropic API Key set in environment variables (usually `ANTHROPIC_API_KEY`)

## Step-by-Step Implementation

### Step 1: Define Your Tool
Tools are defined using a JSON schema. In the Anthropic SDK, this is passed via the `tools` parameter in a `messages.create` call.

```python
from anthropic.types import ToolParam

get_weather_tool = {
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
            }
        },
        "required": ["location"]
    }
}
```

### Step 2: Provide Tools to Claude
Pass your tool definitions in the `tools` list when creating a message.

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    tools=[get_weather_tool],
    messages=[{"role": "user", "content": "What's the weather like in San Francisco?"}]
)
```

### Step 3: Handle Tool Use Requests
If Claude decides to use a tool, the response's `stop_reason` will be `"tool_use"`. You need to iterate through the `content` blocks to find the `tool_use` request.

```python
if response.stop_reason == "tool_use":
    tool_use = next(block for block in response.content if block.type == "tool_use")
    tool_name = tool_use.name
    tool_input = tool_use.input
    tool_id = tool_use.id
    
    # Execute your local function with tool_input
    # result = my_local_function(**tool_input)
```

### Step 4: Return Tool Results
To continue the conversation, send the tool output back to Claude. The message must have the `role: "user"` and contain a `tool_result` block.

```python
# Add the assistant's tool_use message to your history
messages.append({"role": "assistant", "content": response.content})

# Add the tool result message
messages.append({
    "role": "user",
    "content": [
        {
            "type": "tool_result",
            "tool_use_id": tool_id,
            "content": str(result), # The output of your function
        }
    ]
})

# Get the final response from Claude
final_response = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    tools=[get_weather_tool],
    messages=messages
)
```

## Practical Example

Check the [001_tools_007.ipynb](file:///Users/d3vil/Documents/projects/ac/tools/001_tools_007.ipynb) notebook in this directory for a complete working example using the `anthropic` SDK, including a helper `chat` function and a simple datetime tool.

## Key Differences from Other APIs (e.g., Groq/OpenAI)

| Feature | Anthropic (Claude) | OpenAI / Groq |
| :--- | :--- | :--- |
| **Schema Field** | `input_schema` | `parameters` |
| **Tool Response Role** | `user` | `tool` |
| **Tool Tracking** | `tool_use_id` | `tool_call_id` |
| **SDK Method** | `client.messages.create` | `client.chat.completions.create` |

---
*For more information, refer to the [Anthropic Tool Use Documentation](https://docs.anthropic.com/en/docs/build-with-claude/tool-use).*
