"""create users,chats,messages table

Revision ID: ac89aba21397
Revises: 60cd20025d33
Create Date: 2025-09-10 03:45:11.525197

"""
from typing import Sequence, Union
import uuid
from sqlalchemy.dialects.postgresql import UUID
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ac89aba21397'
down_revision: Union[str, Sequence[str], None] = '60cd20025d33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('full_name', sa.Text, nullable=False),
        sa.Column('phone_number', sa.String(20), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Create chats table
    op.create_table(
        'chats',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('session_id', sa.String(100), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False), 
        sa.Column('message_id', UUID(as_uuid=True), sa.ForeignKey('messages.id'), nullable=False),  # Relates chats to messages
        sa.Column('sender', sa.String(20), nullable=False),  # 'client' or 'system'
        sa.Column('timestamp', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('status', sa.String(50), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade():
    # Drop new tables
    op.drop_table('chats')
    op.drop_table('messages')
    op.drop_table('users')