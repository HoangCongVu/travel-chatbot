""" users,chats,messages table

Revision ID: 29585792512f
Revises: 6c875b46eb82
Create Date: 2025-09-10 06:14:38.501504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '29585792512f'
down_revision: Union[str, Sequence[str], None] = '6c875b46eb82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=sa.func.uuid_generate_v4(), nullable=False),
        sa.Column('full_name', sa.Text, nullable=False),
        sa.Column('phone_number', sa.String(20), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    op.create_table(
        'chats',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('session_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.Text, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    op.create_table(
        'messages',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('chat_id', sa.UUID(as_uuid=True), sa.ForeignKey('chats.id'), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('role', sa.Text, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

def downgrade():
    op.drop_table('messages', if_exists=True)
    op.drop_table('chats', if_exists=True)
    op.drop_table('users', if_exists=True)