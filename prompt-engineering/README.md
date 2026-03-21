# Prompt Engineering Lessons Learned

This document summarizes the best practices, techniques, and "hard-won" lessons learned during the prompt engineering of this project.

## 1. Iterative Prompt Engineering Process

Our workflow follows a structured cycle:
1.  **Generate**: Draft the prompt and model persona.
2.  **Test**: Run the prompt against a diverse dataset of scenarios.
3.  **Evaluate**: Grade the output with a deterministic model (Temperature 0.0) against mandatory criteria.
4.  **Refine**: Update the prompt based on evaluation reasoning.

## 2. API Parameter Optimization

Different tasks require specific parameter configurations:

| Parameter | Recommended Value | Use Case |
| :--- | :--- | :--- |
| **`stop`** | `["```"]` or `["\n"]` | Crucial for stopping the model after a code block or JSON object. |
| **`temperature`** | `1.0` | **Creative Generation**: Unique ideas, brainstorming. |
| **`temperature`** | `0.7` | **Balanced Tasks**: Generating test cases, explanations. |
| **`temperature`** | `0.0` | **Deterministic Tasks**: Grading, logical evaluation, JSON extraction. |

> [!IMPORTANT]
> **Groq/OpenAI Quirk**: Always use `stop` as the parameter name. Older or custom wrappers might use `stop_sequences`, which can cause `TypeError` if not handled correctly.

## 3. Prompt Structuring with XML-like Tags

Separating prompt sections using XML-like tags (e.g., `<task_description>`, `<task_inputs>`) significantly improves model performance:
-   **Eliminates Ambiguity**: Clear distinction between instructions and data.
-   **Focuses the Model**: Helps the model identify the core task versus context.
-   **Example Structure**:
    ```text
    <task_description>
    Summarize the following medical report.
    </task_description>

    <task_inputs>
    {report_content}
    </task_inputs>
    ```

## 4. Controlled JSON Output

To ensure reliable, parsable JSON:
1.  **Direct Instructions**: Use phrases like "Respond with ONLY a structured JSON object."
2.  **Provide a Schema/Shape**: Explicitly define the expected fields.
    ```json
    {
        "reasoning": "string",
        "score": "number (1-10)"
    }
    ```
3.  **Template Escaping**: When using Python f-strings or Jinja-like templates, escape literal braces as `{{` and `}}` to avoid collision with variables.
4.  **Assistant Pre-filling**: Pre-fill the start of the assistant's response with "```json" to force the model into the right mode.

## 5. Few-Shot Prompting

When a task is complex, provide `<sample_input>` and `<ideal_output>` within the prompt. This "few-shot" approach is often more effective than long, descriptive instructions.

## 6. Rigorous Evaluation Strategies

For automated grading:
-   **Personas**: Assign a persona like "You are an expert evaluator with extreme rigor."
-   **Mandatory Requirements**: Use `<extra_important_criteria>` tags to list deal-breakers.
-   **Automatic Failure**: Instruct the model that ANY violation of mandatory criteria must result in a failing score (e.g., 3/10 or lower).
