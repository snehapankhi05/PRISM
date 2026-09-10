from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PRISM"
    environment: str = "development"
    debug: bool = True

    api_host: str = "127.0.0.1"
    api_port: int = 8000

    database_url: str = ""

    llm_provider: str = "groq"
    llm_api_key: str = ""

    embedding_provider: str = "local"
    vector_db: str = "chroma"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="PRISM_",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()