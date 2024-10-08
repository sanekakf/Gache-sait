"""empty message

Revision ID: e5a304e9340e
Revises: ab195f39f10d
Create Date: 2021-09-02 23:19:15.373939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5a304e9340e'
down_revision = 'ab195f39f10d'
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
