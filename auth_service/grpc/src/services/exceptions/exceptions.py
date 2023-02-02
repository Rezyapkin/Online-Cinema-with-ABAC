class CustomBaseError(Exception):
    ERROR_MESSAGE: str

    def __init__(self):
        super().__init__(self.ERROR_MESSAGE)


class UserNotFoundError(CustomBaseError):
    """Exception raised if user not found."""

    ERROR_MESSAGE = "User not found!"


class UserDisabledError(CustomBaseError):
    """Exception raised if user disabled."""

    ERROR_MESSAGE = "User is disabled!"


class UserNotSuperuserError(CustomBaseError):
    """Exception raised if user is not superuser or super is disabled."""

    ERROR_MESSAGE = "User is not superuser!"


class UserEmailCollisionError(CustomBaseError):
    """Exception is raised if email is already in use by other user."""

    ERROR_MESSAGE = "Email is already in use!"


class UserEmailUpdateSameError(CustomBaseError):
    """Exception is raised if updated email is same as current."""

    ERROR_MESSAGE = "Email is same!"


class UserPasswordInvalidError(CustomBaseError):
    """Exception is raised if password doesn't match hashed in DB."""

    ERROR_MESSAGE = "Password not valid!"


class UserPasswordUpdateSameError(CustomBaseError):
    """Exception is raised if updated password is same as current."""

    ERROR_MESSAGE = "Password is same!"


class UserHistoryPageNotFoundError(CustomBaseError):
    """Exception raised if user login history page not found."""

    ERROR_MESSAGE = "Login history page not found!"


class UserListPageNotFoundError(CustomBaseError):
    """Exception raised if users page not found."""

    ERROR_MESSAGE = "Users page not found!"


class PolicyListPageNotFoundError(CustomBaseError):
    """Exception raised if policies page not found."""

    ERROR_MESSAGE = "Policy page not found!"


class BaseTokenError(CustomBaseError):
    """Base token exception."""

    ...


class TokenInvalidError(BaseTokenError):
    """Exception is raised if token parse failed."""

    ERROR_MESSAGE = "Invalid token!"


class TokenExpiredError(BaseTokenError):
    """Exception is raised if token expired."""

    ERROR_MESSAGE = "Token expired!"


class TokenInvalidUserAgentError(BaseTokenError):
    """Exception is raised if token user_agent doesn't match request user_agent."""

    ERROR_MESSAGE = "Invalid user agent for requested token!"


class AccessTokenBannedError(BaseTokenError):
    """Exception is raised if access token in blacklist."""

    ERROR_MESSAGE = "Access token banned!"


class AccessTokenCannotBeUsedAsRefreshTokenError(BaseTokenError):
    """Exception is raised if access token is used as refresh."""

    ERROR_MESSAGE = "Access token cannot be used as refresh token!"


class RefreshTokenUnknownError(BaseTokenError):
    """Exception is raised if refresh token not found in whitelist or doesn't match signature in user cache."""

    ERROR_MESSAGE = "Refresh token unknown!"


class RefreshTokenCannotBeUsedAsAccessTokenError(BaseTokenError):
    """Exception is raised if refresh token is used as access."""

    ERROR_MESSAGE = "Refresh token cannot be used as access token!"


class PolicyBadFormattedError(CustomBaseError):
    """Exception is raised if policy cannot be deserialized to Policy object."""

    ERROR_MESSAGE = "Policy bad formatted!"


class PolicyAlreadyExistsError(CustomBaseError):
    """Exception is raised if policy already exists."""

    ERROR_MESSAGE = "Policy already exists!"


class PolicyNotFoundError(CustomBaseError):
    """Exception raised if policy not found."""

    ERROR_MESSAGE = "Policy not found!"
