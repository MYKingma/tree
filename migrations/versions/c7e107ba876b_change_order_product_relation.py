"""change order product relation

Revision ID: c7e107ba876b
Revises: e9c932708073
Create Date: 2020-09-09 16:40:23.215991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7e107ba876b'
down_revision = 'e9c932708073'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'products', ['product_id'], ['id'])
        batch_op.drop_column('order')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order', sa.VARCHAR(length=128), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('product_id')

    # ### end Alembic commands ###
