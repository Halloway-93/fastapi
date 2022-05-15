"""add content column

Revision ID: 09cc9dc6a1e6
Revises: 84792a055a0e
Create Date: 2022-05-08 19:14:35.428389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "09cc9dc6a1e6"
down_revision = "84792a055a0e"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
