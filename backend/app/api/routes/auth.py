from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db_session
from app.schemas.user import UserPublicResponse, UserRegistrationRequest
from app.services.exceptions import (
    DuplicateEmailError,
    DuplicateUserError,
    DuplicateUsernameError,
)
from app.services.registration_service import RegistrationService

router = APIRouter()

DatabaseSession = Annotated[Session, Depends(get_db_session)]


@router.post(
    "/register",
    response_model=UserPublicResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new SentinelAI user",
)
def register_user(
    request: UserRegistrationRequest,
    session: DatabaseSession,
) -> UserPublicResponse:
    """Create a user account without automatically logging it in."""

    service = RegistrationService(session)

    try:
        user = service.register(request)

    except DuplicateEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        ) from exc

    except DuplicateUsernameError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This username is already in use",
        ) from exc

    except DuplicateUserError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with these details already exists",
        ) from exc

    return UserPublicResponse.model_validate(user)
