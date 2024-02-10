class AuthenticationError(Exception):
    pass


class UserNotFoundError(AuthenticationError):
    pass


class UserInvalidPassword(AuthenticationError):
    pass