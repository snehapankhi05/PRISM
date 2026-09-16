import json
from typing import TypeVar

from groq import Groq
from pydantic import BaseModel

from backend.app.services.llm.base import LLMProvider


T = TypeVar("T", bound=BaseModel)


class GroqLLMProvider(LLMProvider):
    def __init__(
        self,
        api_key: str,
        model: str,
    ):
        self.client = Groq(api_key=api_key)
        self.model = model

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
    ) -> str:
        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return response.choices[0].message.content or ""

    def generate_structured(
        self,
        prompt: str,
        response_model,
        *,
        system_prompt: str | None = None,
    ):
        schema = response_model.model_json_schema()

        system = system_prompt or ""

        system += """
You are a structured data extraction engine.

You MUST return a valid JSON object.

Rules:
- Return JSON only.
- Do not return markdown.
- Do not return ```json fences.
- Do not return explanations.
- Do not return an empty response.
- Follow the provided JSON schema exactly.
- Every required field must be present.
- Keep strings concise.
- Do not add unnecessary details.
- Use only information supported by the provided source.
"""

        user_prompt = f"""
{prompt}

Return ONLY valid JSON matching this schema:

{json.dumps(schema, indent=2)}

IMPORTANT:
- Output JSON only.
- No markdown.
- No ```json fences.
- No explanation.
- Every required field must be present.
- Keep strings concise.
- Do not add unnecessary details.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0,
            max_tokens=8192,
        )

        choice = response.choices[0]
        message = choice.message

        raw_content = (message.content or "").strip()

        if not raw_content:
            raise ValueError(
                "LLM returned empty structured output. "
                f"finish_reason={choice.finish_reason}, "
                f"model={self.model}"
            )

        # Remove markdown fences if the model ignores the instruction.
        if raw_content.startswith("```"):
            lines = raw_content.splitlines()

            if lines and lines[0].strip().startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            raw_content = "\n".join(lines).strip()

        # Parse JSON.
        try:
            parsed = json.loads(raw_content)

        except json.JSONDecodeError as exc:
            raise ValueError(
                "LLM returned invalid JSON. "
                f"finish_reason={choice.finish_reason}, "
                f"model={self.model}\n"
                f"{raw_content[:2000]}"
            ) from exc

        # Validate against the Pydantic response model.
        try:
            return response_model.model_validate(parsed)

        except Exception as exc:
            raise ValueError(
                "LLM JSON does not match the expected schema:\n"
                f"{raw_content[:2000]}"
            ) from exc