from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRegistrationRequest
from app.services.exceptions import (
    DuplicateEmailError,
    DuplicateUserError,
    DuplicateUsernameError,
)


class RegistrationService:
    """Application service for user registration."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._users = UserRepository(session)

    def register(self, request: UserRegistrationRequest) -> User:
        if self._users.get_by_email(request.email) is not None:
            raise DuplicateEmailError

        if self._users.get_by_username(request.username) is not None:
            raise DuplicateUsernameError

        encoded_password = hash_password(request.password)

        try:
            user = self._users.create(
                username=request.username,
                email=request.email,
                password_hash=encoded_password,
            )

            self._session.commit()
            self._session.refresh(user)

        except IntegrityError as exc:
            self._session.rollback()
            self._raise_classified_conflict(exc)

        return user

    @staticmethod
    def _raise_classified_conflict(exc: IntegrityError) -> None:
        constraint_name = getattr(
            getattr(exc, "orig", None),
            "diag",
            None,
        )

        resolved_name = getattr(constraint_name, "constraint_name", None)

        if resolved_name == "uq_users_email":
            raise DuplicateEmailError from exc

        if resolved_name == "uq_users_username":
            raise DuplicateUsernameError from exc

        raise DuplicateUserError from exc
