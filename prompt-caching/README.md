# Prompt Caching with Claude

Prompt Caching allows you to store frequently used context (like system prompts, large documents, or tool definitions) and reuse it across multiple API calls. This significantly reduces costs and improves latency for repetitive tasks.

## 🚀 Key Benefits

- **Cost Savings**: Cached reads are up to **90% cheaper** than standard input tokens.
- **Improved Latency**: Reusing cached context skips the pre-processing phase, leading to faster response times.
- **Large Context Support**: Ideal for long-running conversations, RAG with static knowledge bases, and complex agentic workflows.

## 💰 Pricing Structure

Pricing is split into **Cache Writes** (storing new data) and **Cache Reads** (using existing data).

| Operation | Cost (Multipler of Base Input) | Benefit |
| :--- | :--- | :--- |
| **Standard Input** | 1.0x | Default processing |
| **Cache Write** | ~1.25x | Storing for future use (5m TTL) |
| **Cache Read** | **~0.1x** | Using stored context |

> [!NOTE]
> Values are approximate based on current Anthropic pricing. Write costs are slightly higher to account for the storage and overhead, while Read costs are drastically reduced.

## 🛠 How it Works: Cache Breakpoints

Caching is enabled by adding "breakpoints" using the `cache_control` parameter. When Claude sees this, it checks if the preceding content (a "prefix") is already in the cache.

### Use Case: System Prompt Caching
Perfect for long instructions that remain constant.

```python
# System prompt caching
params["system"] = [
    {
        "type": "text",
        "text": long_system_prompt,
        "cache_control": {"type": "ephemeral"}
    }
]
```

### Use Case: Tool Caching
Ideal for agents with dozens of tool definitions.

```python
# Caching the last tool to capture the whole tool block
tools[-1]["cache_control"] = {"type": "ephemeral"}
```

## 📋 Best Practices & Limits

- **Minimum Tokens**: Content must meet a minimum size to be cacheable (e.g., 1024 tokens for Sonnet/Haiku, 4096 for Opus).
- **Time to Live (TTL)**: The default TTL is **5 minutes**, which refreshes each time the cache is hit.
- **Breakpoint Limit**: You can set up to **4 breakpoints** per request.
- **Cumulative Nature**: Caching follows a prefix-matching logic. If you change anything before a breakpoint, the cache for that breakpoint (and all subsequent ones) will miss.
- **Model Specific**: Caches are unique to each model version (e.g., Sonnet 3.5 vs. Sonnet 4.5).

## 💻 Implementation Example

Based on `caching.ipynb`, here is how to wrap a chat request with caching:

```python
def cached_chat(messages, system=None, tools=None):
    params = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 4000,
        "messages": messages,
    }

    if system:
        params["system"] = [{
            "type": "text", 
            "text": system, 
            "cache_control": {"type": "ephemeral"}
        }]

    if tools:
        # Cache the tool definitions
        tools[-1]["cache_control"] = {"type": "ephemeral"}
        params["tools"] = tools

    return client.messages.create(**params)
```
