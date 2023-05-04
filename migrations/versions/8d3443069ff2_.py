"""empty message

Revision ID: 8d3443069ff2
Revises: ec95758a8920
Create Date: 2023-05-05 00:51:57.229836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d3443069ff2'
down_revision = 'ec95758a8920'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    # ### end Alembic commands ###
