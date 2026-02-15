"""init
Revision ID: 0001_init
Revises:
Create Date: 2026-02-14
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "churches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    op.create_table(
        "volunteers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("church_id", sa.Integer(), sa.ForeignKey("churches.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=False),
        sa.Column("is_leader", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("church_id", "phone", name="uq_volunteer_church_phone"),
    )

    op.create_table(
        "departments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("church_id", sa.Integer(), sa.ForeignKey("churches.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("church_id", "name", name="uq_department_church_name"),
    )

    op.create_table(
        "schedules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("church_id", sa.Integer(), sa.ForeignKey("churches.id", ondelete="CASCADE"), nullable=False),
        sa.Column("service_date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    op.create_table(
        "schedule_assignments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("church_id", sa.Integer(), sa.ForeignKey("churches.id", ondelete="CASCADE"), nullable=False),
        sa.Column("schedule_id", sa.Integer(), sa.ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False),
        sa.Column("volunteer_id", sa.Integer(), sa.ForeignKey("volunteers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("department_id", sa.Integer(), sa.ForeignKey("departments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="PENDING"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("schedule_id", "volunteer_id", "department_id", name="uq_assignment_unique"),
    )

    op.create_table(
        "confirmations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("church_id", sa.Integer(), sa.ForeignKey("churches.id", ondelete="CASCADE"), nullable=False),
        sa.Column("schedule_assignment_id", sa.Integer(), sa.ForeignKey("schedule_assignments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("received_text", sa.String(length=255), nullable=False),
        sa.Column("result_status", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    op.create_table(
        "logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("level", sa.String(length=16), nullable=False, server_default="INFO"),
        sa.Column("message", sa.String(length=500), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

def downgrade():
    op.drop_table("logs")
    op.drop_table("confirmations")
    op.drop_table("schedule_assignments")
    op.drop_table("schedules")
    op.drop_table("departments")
    op.drop_table("volunteers")
    op.drop_table("churches")
