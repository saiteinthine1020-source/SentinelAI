"""initialize migration foundation

Revision ID: e8b2fcf5c4c5
Revises:
Create Date: 2026-07-13 17:09:27.230005

"""

from collections.abc import Sequence

revision: str = "e8b2fcf5c4c5"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
