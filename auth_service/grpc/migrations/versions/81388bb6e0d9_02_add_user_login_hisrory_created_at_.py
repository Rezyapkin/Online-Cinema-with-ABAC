"""02_add_user_login_hisrory_created_at_partition

Revision ID: 81388bb6e0d9
Revises: f3ae0e57ecab
Create Date: 2023-01-22 17:11:44.017931

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "81388bb6e0d9"
down_revision = "f3ae0e57ecab"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        """
            CREATE TABLE IF NOT EXISTS
                "user_login_history_2023"
            PARTITION OF
                "user_login_history"
            FOR VALUES
                FROM ('2023-1-1 00:00:00') TO ('2024-1-1 00:00:00')
        """
    )
    op.execute(
        """
            CREATE TABLE IF NOT EXISTS
                "user_login_history_2024"
            PARTITION OF
                "user_login_history"
            FOR VALUES
                FROM ('2024-1-1 00:00:00') TO ('2025-1-1 00:00:00')
        """
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        """
            DROP TABLE IF EXISTS
                "user_login_history_2023"
        """
    )
    op.execute(
        """
            DROP TABLE IF EXISTS
                "user_login_history_2024"
        """
    )
    # ### end Alembic commands ###
