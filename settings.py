import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import SecretStr, StrictStr

load_dotenv()


class SiteSettings(BaseSettings):
    api_key: SecretStr = os.getenv("SITE_API")
    host_api: StrictStr = os.getenv("HOST_API")


class BotSettings(BaseSettings):
    bot_key: SecretStr = os.getenv("BOT_TOKEN")
