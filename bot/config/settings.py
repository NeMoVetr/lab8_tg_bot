import os
from dataclasses import field, dataclass
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv, find_dotenv


@dataclass
class BotSettings:
    token: str = field(default_factory=lambda: os.getenv("BOT_TOKEN"))


@dataclass
class VectorDBSettings:
    path: str = field(default_factory=lambda: os.getenv("VECTOR_DB_PATH"))


@dataclass
class OpenAISettings:
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))


@dataclass
class TavilySettings:
    api_key: str = field(default_factory=lambda: os.getenv("TAVILY_API_KEY"))


@dataclass
class Settings:
    bot: BotSettings = field(default_factory=BotSettings)
    vector_db: VectorDBSettings = field(default_factory=VectorDBSettings)
    openai: OpenAISettings = field(default_factory=OpenAISettings)
    tevily: TavilySettings = field(default_factory=TavilySettings)

    @classmethod
    def from_env(cls) -> "Settings":
        # найдём .env где бы ни запускался скрипт
        env_file = find_dotenv(raise_error_if_not_found=True)
        load_dotenv(env_file)
        return Settings()


@lru_cache(maxsize=1, typed=True)
def get_settings() -> Settings:
    return Settings.from_env()
