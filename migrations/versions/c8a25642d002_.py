"""empty message

Revision ID: c8a25642d002
Revises: c05ec2e9e67c
Create Date: 2023-11-27 20:46:40.022867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8a25642d002'
down_revision = 'c05ec2e9e67c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('district_psychiatric_center', schema=None) as batch_op:
        batch_op.add_column(sa.Column('visitor_postal_code', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('postal_postal_code', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('district_psychiatric_center', schema=None) as batch_op:
        batch_op.drop_column('postal_postal_code')
        batch_op.drop_column('visitor_postal_code')

    # ### end Alembic commands ###