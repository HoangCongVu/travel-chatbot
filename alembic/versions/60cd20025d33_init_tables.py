"""init tables

Revision ID: 60cd20025d33
Revises: 
Create Date: 2025-09-03 09:22:26.201329

"""
from typing import Sequence, Union
import uuid
from sqlalchemy.dialects.postgresql import UUID
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60cd20025d33'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # tour_types
    op.create_table(
        'tour_types',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('type_name', sa.Text, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    # tours
    op.create_table(
        'tours',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('tour_name', sa.Text, nullable=False),
        sa.Column('tour_type_id', sa.Integer, sa.ForeignKey('tour_types.id'), nullable=False),
        sa.Column('days', sa.Integer, nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('highlight', sa.Text, nullable=True),
        sa.Column('itinerary_url', sa.Text, nullable=True),
        sa.Column('detail_url', sa.Text, nullable=True),
        sa.Column('promotion_info', sa.Text, nullable=True),
        sa.Column('price_type', sa.String(50), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    # tour_destinations
    op.create_table(
        'tour_destinations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('tour_id', UUID(as_uuid=True), sa.ForeignKey('tours.id'), nullable=False),
        sa.Column('destination_name', sa.Text, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    
    )

    # tour_departures
    op.create_table(
        'tour_departures',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('tour_id', UUID(as_uuid=True), sa.ForeignKey('tours.id'), nullable=False),
        sa.Column('departure_name', sa.Text, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    
    )

    # tour_highlight_locations
    op.create_table(
        'tour_highlight_locations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('tour_id', UUID(as_uuid=True), sa.ForeignKey('tours.id'), nullable=False),
        sa.Column('location_name', sa.Text, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    
    )

    # visa_prices
    op.create_table(
        'visa_prices',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('tour_id', UUID(as_uuid=True), sa.ForeignKey('tours.id'), nullable=False),
        sa.Column('price', sa.Numeric, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    
    )

    # price_by_dates
    op.create_table(
        'price_by_dates',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('tour_id', UUID(as_uuid=True), sa.ForeignKey('tours.id'), nullable=False),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('price', sa.Numeric, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    
    )

    # price_by_packages
    op.create_table(
        'price_by_packages',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('tour_id', UUID(as_uuid=True), sa.ForeignKey('tours.id'), nullable=False),
        sa.Column('package_name', sa.Text, nullable=False),
        sa.Column('price', sa.Numeric, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    
    )

    # departure_schedules
    op.create_table(
        'departure_schedules',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('tour_id', UUID(as_uuid=True), sa.ForeignKey('tours.id'), nullable=False),
        sa.Column('schedule_type', sa.String(50), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    
    )

    # specific_departures
    op.create_table(
        'specific_departures',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('schedule_id', UUID(as_uuid=True), sa.ForeignKey('departure_schedules.id'), nullable=False),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    
    )

    # recurring_schedules
    op.create_table(
        'recurring_schedules',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('schedule_id', UUID(as_uuid=True), sa.ForeignKey('departure_schedules.id'), nullable=False),
        sa.Column('recurrence_type', sa.String(50), nullable=False),
        sa.Column('start_date', sa.Date, nullable=False),
        sa.Column('end_date', sa.Date, nullable=False),
        sa.Column('weekdays', sa.ARRAY(sa.Integer), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    
    )
def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('recurring_schedules')
    op.drop_table('specific_departures')
    op.drop_table('departure_schedules')
    op.drop_table('price_by_packages')
    op.drop_table('price_by_dates')
    op.drop_table('visa_prices')
    op.drop_table('tour_highlight_locations')
    op.drop_table('tour_departures')
    op.drop_table('tour_destinations')
    op.drop_table('tours')
    op.drop_table('tour_types')
