class AuthenticationError(Exception):
    pass


class InvalidUserIdError(AuthenticationError):
    pass


class UserNotFoundError(AuthenticationError):
    pass


class UserInvalidPassword(AuthenticationError):
    pass


class UserLoginError(Exception):
    pass


class UserNotFoundError(UserLoginError):
    pass


class UserInvalidPassword(UserLoginError):
    pass