from pathlib import Path

from app.backend.db.config import DbSettings


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_FILE_PATH = BASE_DIR / '.env'


db_settings = DbSettings(_env_file=ENV_FILE_PATH)