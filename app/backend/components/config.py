import os
from pathlib import Path

from app.backend.db.config import DbSettings
from app.backend.auth.config import AuthSettings
from app.backend.sentry.config import SentrySettings
from app.config import AppSettings, AppModes
from app.bot.config import BotSettings


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "app/backend/pages/templates"

ENV_DIR = BASE_DIR / "secrets" / "environment"
PROD_ENV_FILE_PATH = '/etc/secrets/.prod.env'
DEV_ENV_FILE_PATH = ENV_DIR / '.dev.env'
TEST_ENV_FILE_PATH = ENV_DIR / '.test.env'


match os.getenv("MODE"):
    case AppModes.PROD:
        current_env_file_path = PROD_ENV_FILE_PATH
    case AppModes.DEV:
        current_env_file_path = DEV_ENV_FILE_PATH
    case AppModes.TEST:
        current_env_file_path = TEST_ENV_FILE_PATH
    case _:
        raise RuntimeError("Unknown environment file specified")

db_settings = DbSettings(_env_file=current_env_file_path)
auth_settings = AuthSettings(_env_file=current_env_file_path)
sentry_settings = SentrySettings(_env_file=current_env_file_path)
app_settings = AppSettings(_env_file=current_env_file_path)
bot_settings = BotSettings(_env_file=current_env_file_path)
