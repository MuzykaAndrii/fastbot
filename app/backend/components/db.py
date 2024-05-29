from app.backend.db.session import get_session_maker
from app.backend.components.config import db_settings


async_session_maker = get_session_maker(db_settings)