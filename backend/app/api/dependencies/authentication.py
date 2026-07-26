from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.tokens import (
    TokenExpiredError,
    TokenInvalidError,
    decode_access_token,
)
from app.db.dependencies import get_db_session
from app.models.user import User
from app.repositories.user_repository import UserRepository

DatabaseSession = Annotated[Session, Depends(get_db_session)]


def get_access_token_cookie(
    access_token: Annotated[
        str | None,
        Cookie(alias="sentinelai_access_token"),
    ] = None,
) -> str:
    """Return the JWT cookie or reject unauthenticated requests."""

    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    return access_token


def get_current_user(
    token: Annotated[str, Depends(get_access_token_cookie)],
    session: DatabaseSession,
) -> User:
    """Resolve the active database user represented by the JWT."""

    try:
        payload = decode_access_token(token)

    except (TokenExpiredError, TokenInvalidError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication session",
        ) from exc

    repository = UserRepository(session)
    user = repository.get_by_id(payload.sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication session",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account access is disabled",
        )

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
