from fastapi.middleware import Middleware
from starlette_admin.contrib.sqla import Admin
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.db.session import engine
from .auth import AdminAuthProvider
from app.users.admin.views import UserAdminView
from app.vocabulary.admin.views import LanguagePairAdminView, VocabularyAdminView


admin = Admin(
    engine=engine,
    title="Admin panel",
    debug=settings.DEBUG,
    auth_provider=AdminAuthProvider(),
    middlewares=[Middleware(SessionMiddleware, secret_key=settings.JWT_SECRET)],
)

admin.add_view(UserAdminView())
admin.add_view(VocabularyAdminView())
admin.add_view(LanguagePairAdminView())