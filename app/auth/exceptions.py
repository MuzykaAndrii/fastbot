class AuthenticationError(Exception):
    pass


class InvalidUserIdError(AuthenticationError):
    pass


class UserNotFoundError(AuthenticationError):
    pass


class UserInvalidPassword(AuthenticationError):
    pass