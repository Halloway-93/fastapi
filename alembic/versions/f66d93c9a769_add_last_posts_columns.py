"""add last posts columns

Revision ID: f66d93c9a769
Revises: 3dc52b846fd1
Create Date: 2022-05-15 15:23:06.940922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f66d93c9a769"
down_revision = "3dc52b846fd1"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean, server_default="TRUE", nullable=False),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()")
        ),
    )

    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
