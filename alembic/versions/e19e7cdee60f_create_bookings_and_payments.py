"""create bookings and payments

Revision ID: e19e7cdee60f
Revises: 32a3ce341899
Create Date: 2025-12-02 15:10:48.578981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID 
import uuid  
from sqlalchemy.dialects import postgresql  

# revision identifiers, used by Alembic.
revision: str = 'e19e7cdee60f'
down_revision: Union[str, Sequence[str], None] = '32a3ce341899'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # carts
    op.create_table(
        'carts',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', sa.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('session_id', UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now())
    )

    # cart_items
    op.create_table(
        'cart_items',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('cart_id', UUID(as_uuid=True), sa.ForeignKey('carts.id', ondelete='CASCADE')),
        sa.Column('tour_id', UUID(as_uuid=True), sa.ForeignKey('tours.id'), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('price_snapshot', sa.Numeric(), nullable=False),
        sa.Column('travel_date', sa.Date(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now())
    )
    
    # Tạo bảng bookings
    op.create_table(
        'bookings',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('user_id', sa.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('session_id', UUID(as_uuid=True), nullable=True),
        sa.Column('tour_id', UUID(as_uuid=True), sa.ForeignKey('tours.id'), nullable=False),
        sa.Column('cart_item_id', UUID(as_uuid=True), sa.ForeignKey('cart_items.id'), nullable=False),
        sa.Column('guest_name', sa.String(50), nullable=True),
        sa.Column('guest_phone', sa.String(50), nullable=True),
        sa.Column('guest_email', sa.String(50), nullable=True),
        sa.Column('adult_count', sa.Integer, nullable=False),
        sa.Column('child_count', sa.Integer, nullable=False),
        sa.Column('total_price', sa.Numeric(12,2), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),  # pending/confirmed/cancelled/completed
        sa.Column('special_request', sa.Text, nullable=True),
        sa.Column('meta_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True),
    )

    # Tạo bảng payments
    op.create_table(
        'payments',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('booking_id', UUID(as_uuid=True), sa.ForeignKey('bookings.id'), nullable=False),
        sa.Column('amount', sa.Numeric(12,2), nullable=False),
        sa.Column('payment_method', sa.String(50), nullable=False, server_default='sepay'),
        sa.Column('payment_status', sa.String(20), nullable=False, server_default='pending'),  # pending/processing/success/failed/refunded
        sa.Column('transaction_id', sa.String(255), nullable=True),
        sa.Column('payment_url', sa.String(500), nullable=True),
        sa.Column('meta_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('paid_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


    
def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('payments')
    op.drop_table('bookings')
    op.drop_table('cart_items')
    op.drop_table('carts')
