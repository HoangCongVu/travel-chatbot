"""update tour embedding

Revision ID: 1de05383f31d
Revises: 0583b31972e4
Create Date: 2025-09-18 15:04:43.998953

"""
from typing import Sequence, Union
from pgvector.sqlalchemy import Vector
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1de05383f31d'
down_revision: Union[str, Sequence[str], None] = '0583b31972e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.add_column(
        'tours',
        sa.Column('tour_embedding_vector', Vector(1536), nullable=True)
    )
    op.add_column(
        'tour_departures',
        sa.Column('tour_departure_embedding_vector', Vector(1536), nullable=True)
    )
    op.add_column(
        'tour_destinations',
        sa.Column('tour_destination_embedding_vector', Vector(1536), nullable=True)
    )

def downgrade() -> None:
    op.drop_column('tours', 'tours_embedding_vector')
    op.drop_column('tour_departures', 'tours_departure_embedding_vector')
    op.drop_column('tour_destinations', 'tours_destination_embedding_vector')