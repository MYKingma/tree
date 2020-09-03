"""added short column for update table

Revision ID: d6f350dbd9fe
Revises: 68638249d11c
Create Date: 2020-09-03 14:49:15.555843

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6f350dbd9fe'
down_revision = '68638249d11c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('updates', schema=None) as batch_op:
        batch_op.add_column(sa.Column('body', sa.Text(), nullable=True))
        batch_op.drop_column('description')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('updates', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.drop_column('body')

    # ### end Alembic commands ###