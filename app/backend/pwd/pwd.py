import bcrypt


class PWDService:

    def get_hash(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)

    def verify(self, raw_password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(
            password=raw_password.encode(),
            hashed_password=hashed_password,
        )