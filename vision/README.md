# Computer Vision with Claude

This project explores the multi-modal capabilities of Anthropic's Claude models (specifically `claude-3-7-sonnet-20250219`). It demonstrates how to integrate visual data with text prompts for complex analytical tasks.

## Key Features

- **Multi-modal Message Handling**: Learn how to construct message objects that combine text and base64 encoded images.
- **Complex Analytical Prompts**: Example of using structured, multi-step prompts for specialized visual tasks like satellite imagery analysis.
- **Image Preprocessing**: Helper patterns for encoding local images for API consumption.

## Prompting for Vision (CRITICAL)

One of the most important lessons from this exploration is that **high-quality, structured prompting significantly improves vision analysis results.** 

> [!IMPORTANT]
> Good prompting techniques will give good answers. When asking Claude to analyze an image, be specific about:
> - **What to look for**: List specific features or objects.
> - **Analysis steps**: Break down the task into logical sub-tasks.
> - **Output format**: Define exactly how you want the findings summarized.

See the **Fire Risk Assessment** prompt in the notebook for a practical example of how to guide Claude through a complex visual extraction and rating task.

## Getting Started

### Prerequisites

- Python 3.9+
- Anthropic API Key
- `anthropic` Python SDK
- `python-dotenv` for environment variable management
- `base64` (standard library)

### Setup

1. Navigate to the `vision` directory.
2. Ensure your `.env` file exists in the root with `ANTHROPIC_API_KEY`.
3. Install dependencies:
   ```bash
   pip install anthropic python-dotenv
   ```

### Running the Notebook

The core functionality is demonstrated in [002_images.ipynb](file:///Users/d3vil/Documents/projects/ac/vision/002_images.ipynb).

### Image Format
The API currently supports:
- Image types: `image/jpeg`, `image/png`, `image/gif`, `image/webp`
- Max size: 5MB per image
- Up to 20 images per request

## Example: Encoding and Sending an Image

```python
import base64

with open("image.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

message = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": encoded_string,
                    },
                },
                {"type": "text", "text": "What is in this image?"}
            ],
        }
    ],
)
```
