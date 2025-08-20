"""create users table

Revision ID: ca7d594f80d2
Revises: c11a73252972
Create Date: 2025-08-20 03:15:40.601194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca7d594f80d2'
down_revision: Union[str, Sequence[str], None] = 'c11a73252972'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("phone_number", sa.String(length=20), nullable=False, unique=True),
        sa.Column("email", sa.String(length=100), nullable=True, unique=True),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
