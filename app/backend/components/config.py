from pathlib import Path

from app.backend.db.config import DbSettings
from app.backend.auth.config import AuthSettings
from app.backend.sentry.config import SentrySettings


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_FILE_PATH = BASE_DIR / '.env'


db_settings = DbSettings(_env_file=ENV_FILE_PATH)
auth_settings = AuthSettings(_env_file=ENV_FILE_PATH)
sentry_settings = SentrySettings(_env_file=ENV_FILE_PATH)