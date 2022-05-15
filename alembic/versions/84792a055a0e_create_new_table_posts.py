"""Create new table posts

Revision ID: 84792a055a0e
Revises: 
Create Date: 2022-05-08 18:43:16.504758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "84792a055a0e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
    )
    pass


def downgrade():
    op.drop_table("posts")
    pass
