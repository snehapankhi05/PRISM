from typing import TypeVar

from groq import Groq
from pydantic import BaseModel

from backend.app.services.llm.base import LLMProvider
import json

from pydantic import BaseModel

# ... keep existing imports ...



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
            messages.append({
                "role": "system",
                "content": system_prompt,
            })

        messages.append({
            "role": "user",
            "content": prompt,
        })

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
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt,
            })

        messages.append({
            "role": "user",
            "content": prompt,
        })

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "prism_fact_graph",
                    "strict": False,
                    "schema": response_model.model_json_schema(),
                },
            },
        )

        raw_content = response.choices[0].message.content or "{}"

        return response_model.model_validate(
            json.loads(raw_content)
        )