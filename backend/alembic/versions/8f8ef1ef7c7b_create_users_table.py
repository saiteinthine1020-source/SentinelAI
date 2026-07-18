"""create users table

Revision ID: 8f8ef1ef7c7b
Revises: e8b2fcf5c4c5
Create Date: 2026-07-18 02:38:28.698338

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8f8ef1ef7c7b"
down_revision: str | Sequence[str] | None = "e8b2fcf5c4c5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "email",
            name="uq_users_email",
        ),
        sa.UniqueConstraint(
            "username",
            name="uq_users_username",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
