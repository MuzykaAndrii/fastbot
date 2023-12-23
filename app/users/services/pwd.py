import bcrypt


class PWDService:

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)

    @classmethod
    def verify_password(cls, raw_password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(
            password=raw_password.encode(),
            hashed_password=hashed_password,
        )