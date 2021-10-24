"""empty message

Revision ID: 3070f7341762
Revises: eb36f10cec13
Create Date: 2021-10-23 12:30:06.329449

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3070f7341762'
down_revision = 'eb36f10cec13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=15), nullable=False),
    sa.Column('id_user', sa.String(length=30), nullable=False),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'availability', 'user', ['user'], ['name'], ondelete='CASCADE')
    op.add_column('comment', sa.Column('user', sa.String(length=50), nullable=False))
    op.add_column('favorite', sa.Column('user', sa.String(length=50), nullable=False))
    op.create_foreign_key(None, 'favorite', 'user', ['user'], ['name'])
    op.drop_constraint('reservation_event_id_fkey', 'reservation', type_='foreignkey')
    op.drop_constraint('reservation_user_id_fkey', 'reservation', type_='foreignkey')
    op.drop_column('reservation', 'user_id')
    op.drop_column('reservation', 'event_id')
    op.drop_column('reservation', 'event_name')
    op.create_unique_constraint(None, 'user', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.add_column('reservation', sa.Column('event_name', sa.VARCHAR(length=30), autoincrement=False, nullable=False))
    op.add_column('reservation', sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('reservation', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('reservation_user_id_fkey', 'reservation', 'user', ['user_id'], ['id'])
    op.create_foreign_key('reservation_event_id_fkey', 'reservation', 'event', ['event_id'], ['id'])
    op.drop_constraint(None, 'favorite', type_='foreignkey')
    op.drop_column('favorite', 'user')
    op.drop_column('comment', 'user')
    op.drop_constraint(None, 'availability', type_='foreignkey')
    op.drop_table('profile')
    # ### end Alembic commands ###
