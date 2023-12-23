from fastapi.middleware import Middleware
from starlette_admin.contrib.sqla import Admin
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.db.session import engine
from app.admin.auth import AdminAuthProvider


admin = Admin(
    engine=engine,
    title="Admin panel",
    debug=settings.DEBUG,
    auth_provider=AdminAuthProvider(),
    middlewares=[Middleware(SessionMiddleware, secret_key=settings.JWT_SECRET)],
)