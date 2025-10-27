""" user_id nullable in chats

Revision ID: d52ef9171d6a
Revises: 08f28ea05c32
Create Date: 2025-10-17 09:30:54.959054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd52ef9171d6a'
down_revision: Union[str, Sequence[str], None] = '08f28ea05c32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "chats", "user_id",
        existing_type=sa.UUID(),
        nullable=True
    )

def downgrade():
    op.alter_column(
        "chats", "user_id",
        existing_type=sa.UUID(),
        nullable=False
    )