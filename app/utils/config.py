# Other imports
from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class Tz:
    timezone: str


@dataclass
class Db:
    db_host: str
    db_port: int
    db_user: str
    db_database: str
    db_password: str


@dataclass
class Config:
    tg_bot: TgBot
    db: Db
    tg_timezone: Tz


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env("BOT_TOKEN")),
        tg_timezone=Tz(timezone=env("TIMEZONE")),
        db=Db(
            db_host=env("DB_HOST"),
            db_port=env("DB_PORT"),
            db_user=env("DB_USER"),
            db_database=env("DB_DATABASE"),
            db_password=env("DB_PASSWORD"),
        ),
    )


config = load_config(".env")
