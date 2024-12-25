from typing import Literal

from .claude import ClaudeNewsSignalExtractor
from .base import BaseNewsSignalExtractor


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
    else:
        raise ValueError(f"Unsupported model provider: {model_provider}")
