
import os
from pathlib import Path
import certifi
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Set the CA bundle path for HTTPS requests
os.environ["SSL_CERT_FILE"] = certifi.where()

BASE_DIR = Path(__file__).resolve().parents[3]
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):

    # LLM providers
    ENABLE_GEMINI: bool = False
    ENABLE_GROQ: bool = False
    ENABLE_OPENAI: bool = False

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "gopal2web.dev@gmail.com"
    SMTP_PASSWORD: str | None = None

    # Gemini
    GOOGLE_API_KEY: str | None = None
    GOOGLE_MODEL: str = "gemini-3.5-flash-lite"

    # Groq
    GROQ_API_KEY: str | None = None
    GROQ_MODEL: str = "openai/gpt-oss-20b"
    GROQ_API_URL: str = "https://api.groq.com/openai/v1"

    # OpenAI
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o"

    # Tavily
    ENABLE_WEB_SEARCH: bool = False
    TAVILY_API_KEY: str | None = None

    # LangSmith
    LANGSMITH_TRACING: bool = False
    LANGSMITH_API_KEY: str | None = None
    LANGSMITH_PROJECT: str = "customer-feedback-dev"

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @model_validator(mode="after")
    def validate_required_settings(self):

        errors = []

        # Gemini validation
        if self.ENABLE_GEMINI:
            if not self.GOOGLE_API_KEY or not self.GOOGLE_API_KEY.strip():
                errors.append("GOOGLE_API_KEY is required")

        # Groq validation
        if self.ENABLE_GROQ:
            if not self.GROQ_API_KEY or not self.GROQ_API_KEY.strip():
                errors.append("GROQ_API_KEY is required")

        # OpenAI validation
        if self.ENABLE_OPENAI:
            if not self.OPENAI_API_KEY or not self.OPENAI_API_KEY.strip():
                errors.append("OPENAI_API_KEY is required")

        # Tavily validation
        if self.ENABLE_WEB_SEARCH:
            if not self.TAVILY_API_KEY or not self.TAVILY_API_KEY.strip():
                errors.append("TAVILY_API_KEY is required")

        # LangSmith validation
        if self.LANGSMITH_TRACING:
            if not self.LANGSMITH_API_KEY or not self.LANGSMITH_API_KEY.strip():
                errors.append("LANGSMITH_API_KEY is required")

        if errors:
            raise ValueError(
                "Configuration validation failed:\n- "
                + "\n- ".join(errors)
            )

        if not any([
            self.ENABLE_GEMINI,
            self.ENABLE_GROQ,
            self.ENABLE_OPENAI
        ]):
            raise ValueError("At least one LLM provider must be enabled")

        return self


settings = Settings()
