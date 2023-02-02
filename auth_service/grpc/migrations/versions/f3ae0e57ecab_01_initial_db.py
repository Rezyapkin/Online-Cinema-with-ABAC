"""01_initial-db

Revision ID: f3ae0e57ecab
Revises:
Create Date: 2023-01-22 17:10:08.759450

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f3ae0e57ecab"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "policy",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("effect", sa.Boolean(), nullable=False),
        sa.Column("context", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("description"),
    )
    op.create_table(
        "user",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=1024), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_table(
        "policy_actions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("policy_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("action", sa.JSON(), nullable=True, comment="JSON value for rule-based policies"),
        sa.ForeignKeyConstraint(["policy_id"], ["policy.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_policy_actions_policy_id"), "policy_actions", ["policy_id"], unique=False)
    op.create_table(
        "policy_resources",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("policy_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("resource", sa.JSON(), nullable=True, comment="JSON value for rule-based policies"),
        sa.ForeignKeyConstraint(["policy_id"], ["policy.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_policy_resources_policy_id"), "policy_resources", ["policy_id"], unique=False)
    op.create_table(
        "policy_subjects",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("policy_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("subject", sa.JSON(), nullable=True, comment="JSON value for rule-based policies"),
        sa.ForeignKeyConstraint(["policy_id"], ["policy.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_policy_subjects_policy_id"), "policy_subjects", ["policy_id"], unique=False)
    op.create_table(
        "user_login_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ip_address", sa.String(length=30), nullable=True),
        sa.Column("user_agent", sa.String(length=256), nullable=True),
        sa.Column("device", postgresql.ENUM("web", "mobile", "smart_tv", name="deviceenum"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", "created_at"),
        postgresql_partition_by="RANGE (created_at)",
    )
    op.create_index(op.f("ix_user_login_history_created_at"), "user_login_history", ["created_at"], unique=False)
    op.create_index(op.f("ix_user_login_history_user_id"), "user_login_history", ["user_id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_login_history_user_id"), table_name="user_login_history")
    op.drop_index(op.f("ix_user_login_history_created_at"), table_name="user_login_history")
    op.drop_table("user_login_history")
    op.drop_index(op.f("ix_policy_subjects_policy_id"), table_name="policy_subjects")
    op.drop_table("policy_subjects")
    op.drop_index(op.f("ix_policy_resources_policy_id"), table_name="policy_resources")
    op.drop_table("policy_resources")
    op.drop_index(op.f("ix_policy_actions_policy_id"), table_name="policy_actions")
    op.drop_table("policy_actions")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_table("policy")
    # ### end Alembic commands ###
