"""added adress and donation

Revision ID: 481a29eb01e7
Revises: 3c3032f2eaf9
Create Date: 2020-10-15 14:53:48.858241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '481a29eb01e7'
down_revision = '3c3032f2eaf9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('donation',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('donation',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###
