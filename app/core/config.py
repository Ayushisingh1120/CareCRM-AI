from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CareCRM AI"
    app_env: str = "development"
    debug: bool = True

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    database_url: str

    llm_provider: str = "openai"

    openai_api_key: str | None = None
    openai_model: str | None = None

    anthropic_api_key: str | None = None
    anthropic_model: str | None = None

    embedding_provider: str = "openai"
    embedding_model: str | None = None

    vector_db: str = "chroma"
    chroma_host: str | None = None
    chroma_port: int | None = None
    chroma_collection: str = "carecrm_knowledge"

    crm_provider: str = "mock"
    crm_api_url: str | None = None
    crm_api_key: str | None = None
    crm_timeout: int = 10

    memory_enabled: bool = True
    max_conversation_messages: int = 20

    confidence_threshold: float = 0.70
    handoff_enabled: bool = True

    secret_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()