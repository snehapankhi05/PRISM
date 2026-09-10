from backend.app.core.config import settings
from backend.app.schemas.fact_graph import FactGraphExtractionResult
from backend.app.services.llm import GroqLLMProvider


def main():
    provider = GroqLLMProvider(
        api_key=settings.llm_api_key,
        model=settings.llm_model,
    )

    result = provider.generate_structured(
        """
Extract one fact from this source:

The incident affected 310 customers.

Return the structured fact graph.
""",
        FactGraphExtractionResult,
        system_prompt=(
            "You are PRISM's Fact Graph extraction engine. "
            "Extract only facts supported by the source."
        ),
    )

    print("Structured extraction successful.")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()