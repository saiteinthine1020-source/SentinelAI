class DuplicateEmailError(Exception):
    """Raised when a user email already exists."""


class DuplicateUsernameError(Exception):
    """Raised when a username already exists."""


class DuplicateUserError(Exception):
    """Raised when a database uniqueness conflict cannot be classified."""


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""


class InactiveUserError(Exception):
    """Raised when an inactive account attempts to log in."""
