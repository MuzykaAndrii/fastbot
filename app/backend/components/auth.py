from app.backend.auth import AuthService
from app.backend.admin.auth import AdminAuthProvider
from app.backend.jwt.jwt import JoseEncoder, Jwt
from .config import auth_settings


jose_jwt_encoder = JoseEncoder(auth_settings.TOKEN_KEY, "HS256")
access_jwt_manager = Jwt(jose_jwt_encoder, auth_settings.ACCESS_TOKEN_LIFETIME_MINUTES)

auth_service = AuthService(access_jwt_manager)
admin_auth_provider = AdminAuthProvider(auth_service)