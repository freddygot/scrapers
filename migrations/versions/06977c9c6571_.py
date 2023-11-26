"""empty message

Revision ID: 06977c9c6571
Revises: 944d60f0f483
Create Date: 2023-11-26 08:52:14.140613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06977c9c6571'
down_revision = '944d60f0f483'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('private_clinic', schema=None) as batch_op:
        batch_op.alter_column('postal_code',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('private_clinic', schema=None) as batch_op:
        batch_op.alter_column('postal_code',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    # ### end Alembic commands ###
