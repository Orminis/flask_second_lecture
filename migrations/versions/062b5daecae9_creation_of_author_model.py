"""creation of author model

Revision ID: 062b5daecae9
Revises: ea9212af7e23
Create Date: 2022-06-26 15:04:07.764361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '062b5daecae9'
down_revision = 'ea9212af7e23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author',
    sa.Column('pk', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('pk')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('author')
    # ### end Alembic commands ###