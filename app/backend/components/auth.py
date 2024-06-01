from app.backend.auth import AuthService
from app.backend.admin.auth import AdminAuthProvider


auth_service = AuthService()
admin_auth_provider = AdminAuthProvider(auth_service)