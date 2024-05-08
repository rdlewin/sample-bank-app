import os
import secrets
from enum import Enum
from typing import Any

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic.v1 import BaseSettings
from pydantic_core import Url

env = os.path.join(os.getcwd(), ".env")
if os.path.exists(env):
    load_dotenv(env)


class Environment(Enum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    ENV: Environment = Environment.LOCAL
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    PROJECT_NAME: str = "Simple Bank API"
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = ""

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return Url.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()  # type: ignore
