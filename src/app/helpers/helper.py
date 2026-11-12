from typing import Literal

from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from app.configs.config import settings
from rich.console import Console

console = Console()

LLMProvider = Literal["gemini", "groq", "openai"]


def get_llm(
    provider: LLMProvider = "gemini",
    temperature: float = 0,
    max_retries: int = 3,
) -> BaseChatModel:
    """
    Create and return an LLM instance based on the selected provider.

    Supported providers:
        - gemini: Google Gemini
        - groq: Groq
        - openai: OpenAI

    Args:
        provider: LLM provider to initialize. Defaults to gemini.
        temperature: Controls response randomness. Defaults to 0.
        max_retries: Maximum retry attempts for failed requests.

    Returns:
        BaseChatModel: Initialized LangChain chat model.

    Raises:
        ValueError: If the provider is unsupported or its API key is missing.
    """

    if provider == "gemini":
        return get_google_llm(
            temperature=temperature,
            max_retries=max_retries,
        )

    if provider == "groq":
        return get_groq_llm(
            temperature=temperature,
            max_retries=max_retries,
        )

    if provider == "openai":
        return get_openai_llm(
            temperature=temperature,
            max_retries=max_retries,
        )

    raise ValueError(f"Unsupported LLM provider: {provider}")


def get_google_llm(
    temperature: float = 0,
    max_retries: int = 3,
) -> ChatGoogleGenerativeAI:
    """
    Create and return a Google Gemini LLM instance.

    Args:
        temperature: Controls response randomness. Defaults to 0.
        max_retries: Maximum retry attempts for failed requests.

    Returns:
        ChatGoogleGenerativeAI: Initialized Gemini model.

    Raises:
        ValueError: If GOOGLE_API_KEY is missing.
    """

    if not settings.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is missing in .env")

    console.print(
        f"[green]Initializing Gemini: {settings.GOOGLE_MODEL}[/green]"
    )

    return ChatGoogleGenerativeAI(
        model=settings.GOOGLE_MODEL,
        google_api_key=settings.GOOGLE_API_KEY,
        max_retries=max_retries,
    )


def get_groq_llm(
    temperature: float = 0,
    max_retries: int = 3,
) -> ChatGroq:
    """
    Create and return a Groq LLM instance.

    Args:
        temperature: Controls response randomness. Defaults to 0.
        max_retries: Maximum retry attempts for failed requests.

    Returns:
        ChatGroq: Initialized Groq model.

    Raises:
        ValueError: If GROQ_API_KEY is missing.
    """

    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing in .env")

    console.print(
        f"[green]Initializing Groq: {settings.GROQ_MODEL}[/green]"
    )

    return ChatGroq(
        model=settings.GROQ_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=temperature,
        max_retries=max_retries,
    )

def get_openai_llm(
    temperature: float = 0,
    max_retries: int = 3,
) -> ChatOpenAI:
    """
    Create and return an OpenAI LLM instance.

    Args:
        temperature: Controls response randomness. Defaults to 0.
        max_retries: Maximum retry attempts for failed requests.

    Returns:
        ChatOpenAI: Initialized OpenAI model.

    Raises:
        ValueError: If OPENAI_API_KEY is missing.
    """

    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing in .env")

    console.print(
        f"[green]Initializing OpenAI: {settings.OPENAI_MODEL}[/green]"
    )

    return ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=temperature,
        max_retries=max_retries,
    )


def get_env_variable(variable_name: str) -> str:
    """
    Retrieve the value of an environment variable from the settings.

    Args:
        variable_name (str): The name of the environment variable to retrieve.
"""
    value = getattr(settings, variable_name, None)
    if value is None:
        raise ValueError(f"Environment variable '{variable_name}' is not set.")
    return value
