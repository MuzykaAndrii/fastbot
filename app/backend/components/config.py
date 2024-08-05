import os
from pathlib import Path

from app.backend.db.config import DbSettings
from app.backend.auth.config import AuthSettings
from app.backend.sentry.config import SentrySettings


ENV_DIR = Path(__file__).resolve().parent.parent.parent.parent / "secrets" / "environment"
PROD_ENV_FILE_PATH = ENV_DIR / '.env.prod'
DEV_ENV_FILE_PATH = ENV_DIR / '.env.dev'
TEST_ENV_FILE_PATH = ENV_DIR / '.env.test'


match os.getenv("MODE"):
    case "PROD":
        CURRENT_ENV_FILE_PATH = PROD_ENV_FILE_PATH
    case "DEV":
        CURRENT_ENV_FILE_PATH = DEV_ENV_FILE_PATH
    case "TEST":
        CURRENT_ENV_FILE_PATH = TEST_ENV_FILE_PATH
    case _:
        raise RuntimeError("Unknown environment file specified")


db_settings = DbSettings(_env_file=CURRENT_ENV_FILE_PATH)
auth_settings = AuthSettings(_env_file=CURRENT_ENV_FILE_PATH)
sentry_settings = SentrySettings(_env_file=CURRENT_ENV_FILE_PATH)
