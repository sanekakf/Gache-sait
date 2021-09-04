"""empty message

Revision ID: faf082dca2ec
Revises: f904417eb8ce
Create Date: 2021-09-02 21:17:35.680147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'faf082dca2ec'
down_revision = 'f904417eb8ce'
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
