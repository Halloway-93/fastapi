"""auto-auto phone numbre

Revision ID: 911ef7fbae6b
Revises: 1d1cba1253a6
Create Date: 2022-05-15 15:51:26.328236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '911ef7fbae6b'
down_revision = '1d1cba1253a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###