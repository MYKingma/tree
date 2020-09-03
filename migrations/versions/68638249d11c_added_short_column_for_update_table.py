"""added short column for update table

Revision ID: 68638249d11c
Revises: ed3f5c53e249
Create Date: 2020-09-03 14:34:36.115041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68638249d11c'
down_revision = 'ed3f5c53e249'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('updates', schema=None) as batch_op:
        batch_op.add_column(sa.Column('short', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('updates', schema=None) as batch_op:
        batch_op.drop_column('short')

    # ### end Alembic commands ###
