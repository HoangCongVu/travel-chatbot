"""init database

Revision ID: 74b227fe734b
Revises: 
Create Date: 2025-08-21 10:45:06.381959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74b227fe734b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # admin_users
    op.create_table(
        'admin_users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('password_hash', sa.Text, nullable=False),
        sa.Column('role', sa.String(20)),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now())
    )
    # users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('full_name', sa.String(100)),
        sa.Column('phone_number', sa.String(20), nullable=False),
        sa.Column('email', sa.String(100)),
        sa.Column('password_hash', sa.Text),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now())
    )

    # departments
    op.create_table(
        'departments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text)
    )

    # doctors
    op.create_table(
        'doctors',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('full_name', sa.String(100)),
        sa.Column('department_id', sa.Integer, sa.ForeignKey('departments.id')),
        sa.Column('specialization', sa.Text),
        sa.Column('biography', sa.Text),
        sa.Column('phone_number', sa.String(20)),
        sa.Column('email', sa.String(100)),
        sa.Column('image_url', sa.Text)
    )

    # services
    op.create_table(
        'services',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('department_id', sa.Integer, sa.ForeignKey('departments.id')),
        sa.Column('description', sa.Text),
        sa.Column('price', sa.Numeric(12, 2))
    )

    # appointments
    op.create_table(
        'appointments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('doctor_id', sa.Integer, sa.ForeignKey('doctors.id')),
        sa.Column('department_id', sa.Integer, sa.ForeignKey('departments.id')),
        sa.Column('appointment_date', sa.Date),
        sa.Column('appointment_time', sa.Time, nullable=False),
        sa.Column('status', sa.String(20)),
        sa.Column('note', sa.Text),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now())
    )

    # schedules
    op.create_table(
        'schedules',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('doctor_id', sa.Integer, sa.ForeignKey('doctors.id')),
        sa.Column('day_of_week', sa.Integer),
        sa.Column('start_time', sa.Time, nullable=False),
        sa.Column('end_time', sa.Time, nullable=False)
    )

    # chat
    op.create_table(
        'chat',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('session_id', sa.Integer),
        sa.Column('title', sa.Text),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now())
    )

    # message
    op.create_table(
        'message',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('chat_id', sa.Integer, sa.ForeignKey('chat.id')),
        sa.Column('content', sa.Text),
        sa.Column('role', sa.Text),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now())
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('message')
    op.drop_table('chat')
    op.drop_table('schedules')
    op.drop_table('appointments')
    op.drop_table('services')
    op.drop_table('doctors')
    op.drop_table('departments')
    op.drop_table('admin_users')
    op.drop_table('users')
