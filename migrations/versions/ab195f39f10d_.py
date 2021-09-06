"""empty message

Revision ID: ab195f39f10d
Revises: 8d1171d82e62
Create Date: 2021-09-02 23:09:24.882550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab195f39f10d'
down_revision = '8d1171d82e62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('password', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('login'),
    sa.UniqueConstraint('login')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###