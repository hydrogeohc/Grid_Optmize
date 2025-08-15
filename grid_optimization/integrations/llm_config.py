"""
LLM Configuration Management

Provides configuration setup for various LLM providers including OpenAI integration
with AIQ toolkit compatibility.
"""

import os
from typing import Optional

from aiq.llm.openai_llm import OpenAIModelConfig


def create_openai_config(
    api_key: Optional[str] = None,
    model_name: str = "gpt-3.5-turbo",
    temperature: float = 0.1,
    max_tokens: int = 1024,
) -> OpenAIModelConfig:
    """
    Create OpenAI model configuration for AIQ integration.

    Args:
        api_key: OpenAI API key. If None, reads from OPENAI_API_KEY env var
        model_name: Model name to use (default: gpt-3.5-turbo)
        temperature: Sampling temperature (default: 0.1)
        max_tokens: Maximum tokens to generate (default: 1024)

    Returns:
        Configured OpenAIModelConfig instance
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key must be provided or set in OPENAI_API_KEY environment variable"
            )

    config = OpenAIModelConfig(
        api_key=api_key, model_name=model_name, temperature=temperature, max_tokens=max_tokens
    )

    return config


def create_grid_llm_config() -> OpenAIModelConfig:
    """
    Create optimized OpenAI configuration for grid optimization tasks.

    Returns:
        OpenAIModelConfig optimized for grid operations
    """
    return create_openai_config(model_name="gpt-4o-mini", temperature=0.1, max_tokens=2048)


def create_advanced_grid_llm_config() -> OpenAIModelConfig:
    """
    Create advanced OpenAI configuration for complex grid analysis.

    Returns:
        OpenAIModelConfig optimized for advanced grid operations
    """
    return create_openai_config(model_name="gpt-4o", temperature=0.1, max_tokens=4096)


# Example usage patterns for reference
def example_usage():
    """Example usage of OpenAI configuration."""

    # Basic configuration
    config = OpenAIModelConfig(api_key="your-openai-api-key", model_name="gpt-3.5-turbo")

    # Advanced configuration
    advanced_config = create_advanced_grid_llm_config()

    # Grid-optimized configuration
    grid_config = create_grid_llm_config()

    return config, advanced_config, grid_config
