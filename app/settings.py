import logging

from pydantic import FieldValidationInfo, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    bot_token: str
    bot_fsm_storage: str
    admins: list[int]
    postgres_dsn: PostgresDsn | None = None
    sqlite_dsn: str | None = None
    redis_dsn: RedisDsn | None = None

    @field_validator("bot_fsm_storage")
    @classmethod
    def validate_fsm_storage(cls, v):
        if v not in ("memory", "redis"):
            raise ValueError(
                "Incorrect 'bot_fsm_storage' value. Value mast be 'memory' or 'redis'"
            )
        return v

    @field_validator("redis_dsn", mode="before")
    @classmethod
    def validate_redis_dsn(cls, v: RedisDsn | None, info: FieldValidationInfo):
        if info.data["bot_fsm_storage"] == "redis" and not v:
            raise ValueError("Redis DSN string is missing!")
        return v

    @field_validator("sqlite_dsn", mode="before")
    @classmethod
    def validate_sqlite_dsn(cls, v: str | None, info: FieldValidationInfo):
        if info.data["postgres_dsn"] is not None:
            return
        return v


settings = Settings()  # type: ignore


def logging_setup(skip_loggers_list: list[str] | None = None):
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s - %(levelname)s %(name)s - "
            "%(module)s:%(funcName)s:%(lineno)s - %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    if skip_loggers_list is not None:
        for logger_name in skip_loggers_list:
            logging.getLogger(logger_name).propagate = False
