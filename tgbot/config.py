from dataclasses import dataclass
from pathlib import Path

from environs import Env
from typing import List


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str




@dataclass
class TgBot:
    token: str
    admin_ids: List[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class I18nData:
    I18N_DOMAIN: str
    LOCALES_DIR: Path


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous
    i18n_data: I18nData




def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    BASE_DIR = Path(__file__).parent.parent


    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous(),
        i18n_data=I18nData(I18N_DOMAIN='testbot', LOCALES_DIR=BASE_DIR / 'locales')
    )
# pg_dump -h 127.0.0.1 -U postgres -F c -f dump.tar.gz gemini_bot
