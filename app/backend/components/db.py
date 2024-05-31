from app.backend.components.config import db_settings
from app.backend.db.session import DataBase


database = DataBase(db_settings)