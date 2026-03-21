# Building with the Claude API: The Comprehensive Guide

This reference guide covers the full spectrum of working with Anthropic's Claude models, from fundamental API operations to advanced agentic workflows and retrieval-augmented generation (RAG).

## 🚀 Claude Model Families

Choose the right model based on your specific task requirements:

| Model | Primary Optimization | Best For... |
| :--- | :--- | :--- |
| **Opus** | Highest Intelligence | Complex reasoning, deep planning, multi-step tasks. |
| **Sonnet** | Balanced (Speed/IQ) | Coding, precise editing, most production use cases. |
| **Haiku** | Speed & Cost | Real-time interaction, high-volume processing, simple tasks. |

> [!TIP]
> **Hybrid Approach**: Use multiple models within a single application—e.g., use Haiku for initial data classification and Opus for the final reasoning step.

---

## 🛠️ Getting Started

### API Request Structure
Requests are made via `client.messages.create()`. Required arguments include `model`, `max_tokens`, and `messages`.

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "How do I build an AI agent?"}]
)
print(message.content[0].text)
```

### Core Configuration
- **System Prompts**: Pass a plain string via the `system` parameter to define Claude's role (e.g., "You are a patient math tutor").
- **Temperature (0–1)**: Controls randomness. Use **0** for factual tasks (deterministic) and **~1** for creative brainstorming.
- **Max Tokens**: A safety limit on generation length, not a target length.

---

## 🧠 Advanced Response Control

### 1. Multi-Turn Conversations
Claude is stateless. You must manually maintain the message list and send the entire history with every request.
- `role: "user"`: Human-authored text.
- `role: "assistant"`: Model-generated responses.

### 2. Pre-filling & Stop Sequences
Steer Claude's response by adding a manual `assistant` message at the end of your message list.
- **Pre-filling**: Provide `"Coffee is better because"` and Claude will continue the sentence.
- **Stop Sequences**: Halt generation when a specific string appears (e.g., stop at `\n` or `###`). Perfect for clean JSON/Code output.

### 3. Response Streaming
Use `stream=True` to receive content chunks in real-time. This provides immediate feedback to users and avoids long "thinking" spinners.

---

## 🔧 Tool Use (Function Calling)

Tool use allows Claude to interact with external APIs and execute logic.

### The 4-Step Cycle
1. **Define**: Create a JSON schema with `input_schema`.
2. **Provide**: Pass schemas in the `tools` parameter.
3. **Handle**: Extract `tool_use` blocks from the response (`stop_reason == "tool_use"`).
4. **Return**: Send back a `tool_result` block in a new `user` message.

### Advanced Tool Techniques
- **Tool Chaining**: Claude uses multiple tools sequentially to solve a problem.
- **Batch Tool**: A meta-tool that allows Claude to request multiple operations in parallel, reducing latency.
- **Fine-Grained Streaming**: Enable `fine_grained: true` to get tool arguments immediately as they are generated.

---

## 🛠️ Built-in Tools (Beta)

Claude Sonnet 4.5 introduces native support for powerful built-in tools that allow the model to interact directly with the environment.

### 1. Text Editor Tool (`text_editor_20250728`)

Provides optimized file system operations, allowing Claude to read, create, and precisely edit files using string-replacement logic (similar to how an engineer would).

**Available Commands:**
- `view`: List directory contents or read specific line ranges of a file.
- `create`: Create a new file with specified content.
- `str_replace`: Perform precise, single-occurrence string replacement.
- `insert`: Insert text at a specific line number.
- `undo_edit`: Revert the last change to a file.

**Sample Schema:**
```python
{
    "type": "text_editor_20250728",
    "name": "str_replace_editor",
}
```

### 2. Web Search Tool (`web_search_20250305`)

Enables real-time data retrieval from the live web. Claude can browse the internet to find current information, research topics, and verify facts.

**Configuration Parameters:**
- `max_uses`: Limit the number of search queries Claude can perform (e.g., `5`).
- `allowed_domains`: Restrict searches to specific authoritative sources (e.g., `["wikipedia.org", "github.com"]`).

**Sample Schema:**
```python
{
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 5,
    "allowed_domains": ["google.com", "anthropic.com"]
}
```

> [!TIP]
> **Tool Use Logic**: Always check `stop_reason == "tool_use"` and process the `tool_use` IDs sequentially to maintain conversation state.

---

## 📚 Retrieval Augmented Generation (RAG)

Query massive datasets (1000+ pages) without hitting context limits by retrieving only relevant chunks.

### The Hybrid Pipeline
1. **Semantic Search**: Use embeddings (e.g., via Voyage AI) to find chunks with similar meanings.
2. **Lexical Search (BM25)**: Match exact keywords and specific terms.
3. **Reciprocal Rank Fusion (RRF)**: Merge results from both searches.
4. **Reranking**: Use an LLM to re-evaluate the top results for final relevance before feeding them to the prompt.

### Contextual Retrieval
Improve accuracy by having Claude add a brief "situating context" to every chunk at indexing time, explaining how it relates to the larger document.

---

## ⚡ Performance & Special Features

### Prompt Caching
Reduce costs and latency by caching static content (system prompts, tool schemas, long documents).
- **Breakpoint**: Add `cache_control: {"type": "ephemeral"}` to up to 4 message blocks.
- **Threshold**: Minimum 1024 tokens required for caching.

### Extended Thinking
For ultra-complex tasks, allocate a **Thinking Budget** (min 1024 tokens). Claude will perform internal reasoning before generating the final answer.

### Vision & Documents
- **Images**: Analyze up to 100 images per request (Base64 or URL).
- **PDFs**: Full support for mixed text, images, and tables via `media_type: "application/pdf"`.
- **Files API**: Upload files once and reference them by ID in future calls.

---

## 🏗️ Systems & Architectures

### Model Context Protocol (MCP)
A standardized communication layer that connects Claude to various data sources (GitHub, Sentry, Jira) without you writing custom tool code. Use **MCP Servers** to expose tools and **MCP Clients** to consume them.

### Agents vs. Workflows
- **Workflows**: Precise, predetermined steps. Use for reliability (e.g., **Evaluator-Optimizer** pattern).
- **Agents**: Dynamic planning using abstract tools. Use for broad, unpredictable tasks where the system must "think" its way to a solution.

---
*Inspired by the Anthropic Course: Building with the Claude API.*
