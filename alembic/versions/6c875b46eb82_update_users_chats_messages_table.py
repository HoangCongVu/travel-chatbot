"""update users,chats,messages table

Revision ID: 6c875b46eb82
Revises: ac89aba21397
Create Date: 2025-09-10 05:42:12.485286

"""
from typing import Sequence, Union
import uuid
from sqlalchemy.dialects.postgresql import UUID
from alembic import op
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6c875b46eb82'
down_revision: Union[str, Sequence[str], None] = 'ac89aba21397'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("DROP TABLE IF EXISTS chats CASCADE;")
    op.execute("DROP TABLE IF EXISTS messages CASCADE;")
    op.execute("DROP TABLE IF EXISTS users CASCADE;")

def downgrade():
    # Nếu cần thì viết lại code tạo bảng, hoặc để pass
    pass

