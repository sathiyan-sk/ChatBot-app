from app.config.settings import get_settings
from app.infrastructure.providers.llm.openrouter_provider import OpenRouterLlmProvider

def main():
    settings = get_settings()
    print("LLM_PROVIDER:", settings.providers.llm)
    print("OpenRouter model:", settings.openrouter.model)
    print("API key present:", bool(settings.openrouter.api_key))

    provider = OpenRouterLlmProvider(settings=settings.openrouter)

    try:
        text = provider.generate(
            system_prompt="You are a helpful assistant.",
            user_prompt="Say hello in one sentence.",
        )
        print("Response:", text)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()