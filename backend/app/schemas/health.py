from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response returned by the basic process health endpoint."""

    status: Literal["ok"]
    service: str
    version: str
    environment: str


class ReadinessResponse(BaseModel):
    """Response returned by the database readiness endpoint."""

    status: Literal["ready"]
    database: Literal["available"]
