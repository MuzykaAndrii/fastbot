from app.backend.auth import AuthService
from app.backend.admin.auth import AdminAuthProvider
from app.backend.jwt.jwt import JoseEncoder, Jwt
from .config import auth_settings
from .services import users_service


jose_jwt_encoder = JoseEncoder(
    key=auth_settings.TOKEN_KEY,
    alg="HS256"
)
access_jwt_manager = Jwt(
    encoder=jose_jwt_encoder,
    lifetime_minutes=auth_settings.ACCESS_TOKEN_LIFETIME_MINUTES,
)

auth_service = AuthService(
    jwt=access_jwt_manager,
    users_service=users_service(),
)
admin_auth_provider = AdminAuthProvider(auth_service)