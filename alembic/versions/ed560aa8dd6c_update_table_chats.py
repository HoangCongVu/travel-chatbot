"""update table chats

Revision ID: ed560aa8dd6c
Revises: d52ef9171d6a
Create Date: 2025-11-11 11:11:38.298947

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed560aa8dd6c'
down_revision: Union[str, Sequence[str], None] = 'd52ef9171d6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('chats', sa.Column('platform', sa.String(length=50), nullable=True))
    op.add_column('chats', sa.Column('external_user_id', sa.String(length=50), nullable=True))


def downgrade() -> None:
    op.drop_column('chats', 'platform')
    op.drop_column('chats', 'external_user_id')
