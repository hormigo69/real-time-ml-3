from typing import Literal

from .base import BaseNewsSignalExtractor
from .claude import ClaudeNewsSignalExtractor
from .ollama import OllamaNewsSignalExtractor


def get_llm(
    model_provider: Literal["anthropic", "ollama"],
) -> BaseNewsSignalExtractor:
    """
    Return the LLM we want for the news signal extraction.

    Args:
        model_provider: The model provider to use for the news signal extraction.

    Returns:
        The LLM we want for the news signal extraction.
    """

    if model_provider == "anthropic":
        from .config import AnthropicConfig

        config = AnthropicConfig()

        return ClaudeNewsSignalExtractor(
            model_name=config.model_name,
            api_key=config.api_key,
        )

    elif model_provider == "ollama":
        from .config import OllamaConfig

        config = OllamaConfig()

        return OllamaNewsSignalExtractor(
            model_name=config.model_name,
        )

    else:
        raise ValueError(f"Unsupported model provider: {model_provider}")
