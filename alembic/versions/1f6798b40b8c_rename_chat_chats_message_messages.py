"""rename chat -> chats, message -> messages

Revision ID: 1f6798b40b8c
Revises: 74b227fe734b
Create Date: 2025-08-21 13:11:10.316374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f6798b40b8c'
down_revision: Union[str, Sequence[str], None] = '74b227fe734b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.rename_table("chat", "chats")
    op.rename_table("message", "messages")

def downgrade() -> None:
    op.rename_table("chats", "chat")
    op.rename_table("messages", "message")