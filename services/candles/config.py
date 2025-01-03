from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    # model_config = SettingsConfigDict(env_file='settings.env')
    model_config = SettingsConfigDict(
        env_file='settings.env', env_file_encoding='utf-8'
    )

    kafka_broker_address: str
    kafka_input_topic: str
    kafka_output_topic: str
    kafka_consumer_group: str
    candle_seconds: int
    max_candles_in_state: int
    emit_incomplete_candles: bool
    data_source: Literal['live', 'historical', 'test']


config = Config()
