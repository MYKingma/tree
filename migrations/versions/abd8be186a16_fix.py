"""fix

Revision ID: abd8be186a16
Revises: a751b5cbdc54
Create Date: 2020-11-11 16:42:10.071322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abd8be186a16'
down_revision = 'a751b5cbdc54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('newsletters', schema=None) as batch_op:
        batch_op.drop_constraint('newsletters_order_id_fkey', type_='foreignkey')
        batch_op.drop_column('order_id')

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('newsletter_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'newsletters', ['newsletter_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('newsletter_id')

    with op.batch_alter_table('newsletters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('newsletters_order_id_fkey', 'orders', ['order_id'], ['id'])

    # ### end Alembic commands ###
