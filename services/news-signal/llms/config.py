from pydantic_settings import BaseSettings, SettingsConfigDict


class AnthropicConfig(BaseSettings):
    model_config = SettingsConfigDict(
        # env_file=Path(__file__).parent / 'anthropic_credentials.env', #it works including the path
        env_file="anthropic_credentials.env",  # it doesn't work
        # env_file='llms/anthropic_credentials.env', # it works including the path hardcoded
        # env_file_encoding='utf-8'
    )
    model_name: str = "claude-3-5-sonnet-20240620"
    api_key: str
