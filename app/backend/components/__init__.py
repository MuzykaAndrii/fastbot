from app.backend.components.unitofwork import UnitOfWork
from app.backend.components.db import database
from app.backend.cookie.cookie import FastAPICookieManager
from app.backend.users.services import UserService
from app.backend.vocabulary.services import VocabularyService
from app.backend.auth import AuthService
from app.backend.admin.auth import AdminAuthProvider
from app.backend.jwt.jwt import JoseEncoder, Jwt
from app.backend.pwd.pwd import PWDService
from .config import auth_settings


jose_jwt_encoder = JoseEncoder(
    key=auth_settings.TOKEN_KEY,
    alg="HS256"
)
access_jwt_manager = Jwt(
    encoder=jose_jwt_encoder,
    lifetime_minutes=auth_settings.ACCESS_TOKEN_LIFETIME_MINUTES,
)

pwd_service = PWDService()

def users_service():
    return UserService(UnitOfWork(database.session_maker), pwd_service)

def vocabularies_service():
    return VocabularyService(UnitOfWork(database.session_maker))

auth_cookie_manager = FastAPICookieManager(auth_settings.TOKEN_NAME)

auth_service = AuthService(
    jwt=access_jwt_manager,
    users_service=users_service,
    pwd_service=pwd_service,
    cookie_manager=auth_cookie_manager,
)
admin_auth_provider = AdminAuthProvider(
    auth_service=auth_service,
    auth_cookie_manager=auth_cookie_manager,
)