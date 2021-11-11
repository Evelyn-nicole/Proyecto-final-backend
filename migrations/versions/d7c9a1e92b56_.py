"""empty message

Revision ID: d7c9a1e92b56
Revises: efbc2c822b26
Create Date: 2021-11-08 23:15:27.420142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7c9a1e92b56'
down_revision = 'efbc2c822b26'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('event', 'availability_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('event', 'superadmin_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('event', 'superadmin_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('event', 'availability_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
