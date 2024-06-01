from fastapi.middleware import Middleware
from starlette_admin.contrib.sqla import Admin
from starlette.middleware.sessions import SessionMiddleware

from app.backend.users.admin.views import UserAdminView
from app.backend.vocabulary.admin.views import LanguagePairAdminView, VocabularyAdminView
from app.config import settings
from app.backend.components.db import database
from app.backend.components.auth import admin_auth_provider


admin = Admin(
    engine=database.engine,
    title="Admin panel",
    debug=settings.DEBUG,
    auth_provider=admin_auth_provider,
    middlewares=[Middleware(SessionMiddleware, secret_key=settings.JWT_SECRET)],
)


admin.add_view(UserAdminView())
admin.add_view(VocabularyAdminView())
admin.add_view(LanguagePairAdminView())