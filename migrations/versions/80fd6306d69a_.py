"""empty message

Revision ID: 80fd6306d69a
Revises: aabc8fbff8bd
Create Date: 2021-09-23 22:02:55.375301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80fd6306d69a'
down_revision = 'aabc8fbff8bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('partners',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('avatarUrl', sa.String(), nullable=True),
    sa.Column('members', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('name'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('partners')
    # ### end Alembic commands ###
