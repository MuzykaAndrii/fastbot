class UserError(Exception):
    pass


class UserNotFoundError(UserError):
    pass


class InvalidUserIdError(UserError):
    pass