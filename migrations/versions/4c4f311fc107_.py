"""empty message

Revision ID: 4c4f311fc107
Revises: 8c05e794e916
Create Date: 2021-09-21 00:21:37.153029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c4f311fc107'
down_revision = '8c05e794e916'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quiz_user_taken', sa.Column('total', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('quiz_user_taken', 'total')
    op.drop_constraint(None, 'quiz_user_answer', type_='foreignkey')
    # ### end Alembic commands ###
