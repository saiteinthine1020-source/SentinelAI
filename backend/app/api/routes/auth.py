from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.dependencies import get_db_session
from app.schemas.user import (
    LoginResponse,
    UserLoginRequest,
    UserPublicResponse,
    UserRegistrationRequest,
)
from app.services.exceptions import (
    DuplicateEmailError,
    DuplicateUserError,
    DuplicateUsernameError,
    InactiveUserError,
    InvalidCredentialsError,
)
from app.services.login_service import LoginService
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


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate a SentinelAI user",
)
def login_user(
    request: UserLoginRequest,
    response: Response,
    session: DatabaseSession,
) -> LoginResponse:
    """Verify credentials and set the access-token cookie."""

    service = LoginService(session)
    settings = get_settings()

    try:
        access_token = service.login(request)

    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        ) from exc

    except InactiveUserError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account access is disabled",
        ) from exc

    response.set_cookie(
        key=settings.access_token_cookie_name,
        value=access_token,
        max_age=settings.access_token_expire_minutes * 60,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        path=settings.cookie_path,
    )

    return LoginResponse(message="Login successful")
