from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.core.tokens import create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserLoginRequest
from app.services.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
)


class LoginService:
    """Application service for user login."""

    def __init__(self, session: Session) -> None:
        self._users = UserRepository(session)

    def login(self, request: UserLoginRequest) -> str:
        user = self._users.get_by_email(request.email)

        if user is None:
            raise InvalidCredentialsError

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise InvalidCredentialsError

        if not user.is_active:
            raise InactiveUserError

        return create_access_token(user_id=user.id)
