class MyJwtError(Exception):
    pass


class JwtMissingError(MyJwtError):
    pass


class JwtNotValidError(MyJwtError):
    pass


class JWTExpiredError(MyJwtError):
    pass