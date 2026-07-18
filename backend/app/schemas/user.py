import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_-]{3,50}$")
UPPERCASE_PATTERN = re.compile(r"[A-Z]")
LOWERCASE_PATTERN = re.compile(r"[a-z]")
NUMBER_PATTERN = re.compile(r"[0-9]")
SPECIAL_PATTERN = re.compile(r"[^A-Za-z0-9]")


class UserRegistrationRequest(BaseModel):
    """Input accepted by the registration endpoint."""

    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        normalized_username = value.strip().lower()

        if not USERNAME_PATTERN.fullmatch(normalized_username):
            raise ValueError(
                "Username may contain only letters, numbers, underscores, and hyphens."
            )

        return normalized_username

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()

    @field_validator("password")
    @classmethod
    def validate_password_policy(cls, value: str) -> str:
        requirements = (
            UPPERCASE_PATTERN.search(value),
            LOWERCASE_PATTERN.search(value),
            NUMBER_PATTERN.search(value),
            SPECIAL_PATTERN.search(value),
        )

        if not all(requirements):
            raise ValueError(
                "Password must include uppercase, lowercase, numeric, and special characters."
            )

        return value


class UserLoginRequest(BaseModel):
    """Input accepted by the login endpoint."""

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_login_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()


class LoginResponse(BaseModel):
    """Safe response returned after successful login."""

    message: str


class UserPublicResponse(BaseModel):
    """Safe public representation of a SentinelAI user."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
