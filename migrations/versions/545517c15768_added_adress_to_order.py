"""added adress to order

Revision ID: 545517c15768
Revises: dc5bd854a50d
Create Date: 2020-10-26 12:10:25.082395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '545517c15768'
down_revision = 'dc5bd854a50d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pickup', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_column('pickup')

    # ### end Alembic commands ###
