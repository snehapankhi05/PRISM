from backend.app.core.config import settings
from backend.app.services.llm import GroqLLMProvider


def main():
    provider = GroqLLMProvider(
        api_key=settings.llm_api_key,
        model=settings.llm_model,
    )

    result = provider.generate(
        "Reply with exactly: PRISM connection successful.",
        system_prompt="You are a test assistant.",
    )

    print(result)


if __name__ == "__main__":
    main()