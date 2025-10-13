"""rename detail_url to image_url

Revision ID: 08f28ea05c32
Revises: 1de05383f31d
Create Date: 2025-10-13 10:18:01.261286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08f28ea05c32'
down_revision: Union[str, Sequence[str], None] = '1de05383f31d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('tours', 'detail_url', new_column_name='image_url')


def downgrade():
    op.alter_column('tours', 'image_url', new_column_name='detail_url')
