"""added adress and donation

Revision ID: 3c3032f2eaf9
Revises: 0eb82e58834d
Create Date: 2020-10-15 14:52:09.649922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c3032f2eaf9'
down_revision = '0eb82e58834d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('donation')

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('donation', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('donation')

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('donation', sa.BOOLEAN(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
