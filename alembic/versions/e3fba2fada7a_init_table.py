"""init table

Revision ID: e3fba2fada7a
Revises: 
Create Date: 2025-08-21 16:03:11.258728

"""
from typing import Sequence, Union
from sqlalchemy.dialects.postgresql import UUID
import uuid
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3fba2fada7a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # admin_users
    op.create_table(
        'admin_users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('password', sa.String(50), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    # users
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('full_name', sa.String(100), nullable=False),
        sa.Column('phone_number', sa.String(20), unique=True, nullable=False),
        sa.Column('email', sa.String(100), unique=True, nullable=False),
        sa.Column('password', sa.String(100), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    # departments
    op.create_table(
        'departments',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('department_name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    # doctors
    op.create_table(
        'doctors',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('full_name', sa.String(100), nullable=False),
        sa.Column('department_id', UUID(as_uuid=True), sa.ForeignKey('departments.id'), nullable=False),
        sa.Column('specialization', sa.Text, nullable=False),
        sa.Column('biography', sa.Text, nullable=False),
        sa.Column('phone_number', sa.String(20), nullable=False),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('image_url', sa.Text, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    # services
    op.create_table(
        'services',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('services_name', sa.String(100), nullable=False),
        sa.Column('department_id', UUID(as_uuid=True), sa.ForeignKey('departments.id'), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('price', sa.Numeric, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False)
    )

    # appointments
    op.create_table(
        'appointments',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('doctor_id', UUID(as_uuid=True), sa.ForeignKey('doctors.id'), nullable=False),
        sa.Column('department_id', UUID(as_uuid=True), sa.ForeignKey('departments.id'), nullable=False),
        sa.Column('appointment_date', sa.Date, nullable=True),
        sa.Column('appointment_time', sa.Time, nullable=True),
        sa.Column('status', sa.String(40), nullable=False),
        sa.Column('note', sa.Text, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False)
    )

    # schedules
    op.create_table(
        'schedules',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('doctor_id', UUID(as_uuid=True), sa.ForeignKey('doctors.id')),
        sa.Column('day_of_week', sa.Integer, nullable=False),
        sa.Column('start_time', sa.Time, nullable=False),
        sa.Column('end_time', sa.Time, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False)
    )

    # chats
    op.create_table(
        'chats',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('session_id', UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False)
    )

    # message
    op.create_table(
        'messages',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('chat_id', UUID(as_uuid=True), sa.ForeignKey('chats.id'), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('role', sa.Text, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False)
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('messages')
    op.drop_table('chats')
    op.drop_table('schedules')
    op.drop_table('appointments')
    op.drop_table('services')
    op.drop_table('doctors')
    op.drop_table('departments')
    op.drop_table('users')
    op.drop_table('admin_users')
 