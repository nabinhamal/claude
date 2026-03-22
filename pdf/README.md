# PDF & Document Analysis with Claude

This project explores Anthropic's native support for PDF and general document analysis. It demonstrates how to send documents to Claude and how to use the advanced **Citations** feature for grounded, verifiable Q&A.

## Key Features

- **Native PDF Support**: Send PDF files directly to Claude using the `document` block type with `media_type: application/pdf`.
- **Structured Document Input**: Send plain text as a logical `document` block, giving it a `title` and scope.
- **Grounded Citations**: Enable `citations: {"enabled": True}` to receive responses that include specific references to the source material.

## Prompting for Documents (CRITICAL)

As with vision and thinking, **better prompting leads to significantly better results.** 

> [!IMPORTANT]
> Good prompting techniques will give good answers. When analyzing documents:
> - **Be specific about the task**: Instead of "Summarize this," try "List the 5 most important financial risks mentioned in this document."
> - **Leverage structure**: Use sections, headings, or specific bullet points in your prompt to guide Claude's focus.
> - **Enable Citations**: When accuracy is paramount, always enable citations to ensure Claude is grounding its answer in the provided text.

## Getting Started

### Prerequisites

- Python 3.9+
- Anthropic API Key
- `anthropic` Python SDK
- `python-dotenv` for environment variable management
- `base64` (standard library)

### Setup

1. Navigate to the `pdf` directory.
2. Ensure your `.env` file exists in the root with `ANTHROPIC_API_KEY`.
3. Install dependencies:
   ```bash
   pip install anthropic python-dotenv
   ```

### Running the Notebooks

- [pdf.ipynb](file:///Users/d3vil/Documents/projects/ac/pdf/pdf.ipynb): Basic PDF encoding and summarization.
- [002_citations_complete.ipynb](file:///Users/d3vil/Documents/projects/ac/pdf/002_citations_complete.ipynb): Advanced document analysis with citations and plain text document blocks.

## Example: Document with Citations

```python
response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "text",
                        "media_type": "text/plain",
                        "data": article_text,
                    },
                    "title": "Earth Article",
                    "citations": {"enabled": True},
                },
                {"type": "text", "text": "How was the moon formed?"}
            ],
        }
    ],
)
```
