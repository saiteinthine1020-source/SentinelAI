from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Database operations for user accounts."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        return self._session.scalar(statement)

    def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)

        return self._session.scalar(statement)

    def create(
        self,
        *,
        username: str,
        email: str,
        password_hash: str,
    ) -> User:
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
        )

        self._session.add(user)
        self._session.flush()

        return user
