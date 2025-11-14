"""add metadata to messages

Revision ID: 3e840e996194
Revises: ed560aa8dd6c
Create Date: 2025-11-14 10:54:32.163719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3e840e996194'
down_revision: Union[str, Sequence[str], None] = 'ed560aa8dd6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'messages',
        sa.Column('meta_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True)
    )

def downgrade() -> None:
    op.drop_column('messages', 'meta_data')