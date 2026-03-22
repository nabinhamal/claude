# Extended Thinking with Claude

This project explores Anthropic's new **Thinking** capability (introduced with Claude 3.7 Sonnet). It provides a laboratory environment to understand how "extended thinking" works, how to configure it via the API, and how to handle its unique output blocks.

## Key Concepts

### 1. Thinking Budget
The `thinking` parameter allows you to enable a dedicated internal chain-of-thought process. You must specify a `budget_tokens` value, which defines the maximum amount of "thinking" Claude can perform before generating its final response.

### 2. Redacted Thinking Blocks
In some cases (e.g., when specific safety triggers are met or the model's internal process is kept private for security reasons), the thinking output is returned as `RedactedThinkingBlock` objects. These blocks contain encrypted/redacted data and cannot be read as plain text.

### 3. Magic Trigger String
A specific "magic string" can be used to test and trigger these redacted thinking behaviors for development and testing purposes.

## Getting Started

### Prerequisites

- Python 3.9+
- Anthropic API Key
- `anthropic` Python SDK
- `python-dotenv` for environment variable management

### Setup

1. Clone the repository and navigate to the `extended-thinking` directory.
2. Create a `.env` file in the root (or parent directory) with your Anthropic key:
   ```env
   ANTHROPIC_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```bash
   pip install anthropic python-dotenv
   ```

### Running the Notebook

The core of this exploration is contained in [001_thinking.ipynb](file:///Users/d3vil/Documents/projects/ac/extended-thinking/001_thinking.ipynb). This notebook demonstrates:

- Initializing the `Anthropic` client with `claude-3-7-sonnet-20250219`.
- Enabling thinking with `thinking={"type": "enabled", "budget_tokens": 1024}`.
- Handling `RedactedThinkingBlock` and `TextBlock` in the API response.
- Chat helper functions for easy experimentation.

## Examples

To enable thinking in your own implementation:

```python
response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=4000,
    thinking={
        "type": "enabled",
        "budget_tokens": 1024,
    },
    messages=[{"role": "user", "content": "How does Quantum Entanglement work?"}]
)
```
