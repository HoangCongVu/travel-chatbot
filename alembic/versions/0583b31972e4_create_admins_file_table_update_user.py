"""create admins, file table, update user

Revision ID: 0583b31972e4
Revises: 29585792512f
Create Date: 2025-09-18 09:51:49.097977

"""

from typing import Sequence, Union
import uuid
from sqlalchemy.dialects.postgresql import UUID
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0583b31972e4'
down_revision: Union[str, Sequence[str], None] = '29585792512f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Thêm password vào bảng users
    op.add_column(
        'users',
        sa.Column('password', sa.String(255), nullable=False)
    )

    # 2. Tạo bảng admins
    op.create_table(
        'admins',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('full_name', sa.Text, nullable=False),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), nullable=False, server_default='admin'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # 3. Tạo bảng files
    op.create_table(
        'files',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('admin_id', sa.UUID(as_uuid=True), sa.ForeignKey('admins.id', ondelete="CASCADE"), nullable=False),
        sa.Column('file_name', sa.Text, nullable=False),
        sa.Column('file_url', sa.Text, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('files')
    op.drop_table('admins')   
    op.drop_column('users', 'password')

