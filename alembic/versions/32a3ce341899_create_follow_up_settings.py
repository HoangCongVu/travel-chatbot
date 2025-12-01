"""create follow_up_settings

Revision ID: 32a3ce341899
Revises: 3e840e996194
Create Date: 2025-11-21 10:18:19.247125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32a3ce341899'
down_revision: Union[str, Sequence[str], None] = '3e840e996194'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'follow_up_settings',
        # 1. ID
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('admin_id', sa.UUID(as_uuid=True), sa.ForeignKey('admins.id', ondelete="SET NULL"), nullable=True),
        # 2. Các cột cấu hình
        sa.Column('is_enabled', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('delay_minutes', sa.Integer(), server_default=sa.text('30'), nullable=False),
        sa.Column('max_count', sa.Integer(), server_default=sa.text('3'), nullable=False),
        sa.Column('active_hours_start', sa.Integer(), server_default=sa.text('8'), nullable=False),
        sa.Column('active_hours_end', sa.Integer(), server_default=sa.text('22'), nullable=False),
        sa.Column('scan_interval_minutes', sa.Integer(), server_default=sa.text('1'), nullable=False),

        # 3. Timestamps
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('follow_up_settings')