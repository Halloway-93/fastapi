"""create foreign_key in post table

Revision ID: 3dc52b846fd1
Revises: 8ead9551f668
Create Date: 2022-05-15 13:27:27.716996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3dc52b846fd1"
down_revision = "8ead9551f668"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade():

    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
