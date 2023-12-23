class JwtMissingError(Exception):
    pass


class JwtNotValidError(Exception):
    pass


class JWTExpiredError(Exception):
    pass