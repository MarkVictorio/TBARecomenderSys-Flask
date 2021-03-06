"""empty message

Revision ID: 1c6724696f49
Revises: db383b517f57
Create Date: 2021-09-21 00:10:13.299259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c6724696f49'
down_revision = 'db383b517f57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    op.create_foreign_key(None, 'quiz_user_answer', 'quiz', ['quiz_id'], ['id'])
    op.add_column('quiz_user_taken', sa.Column('user_total', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('quiz_user_taken', 'user_total')
    op.drop_constraint(None, 'quiz_user_answer', type_='foreignkey')
    op.create_table('post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), nullable=False),
    sa.Column('date_posted', sa.DATETIME(), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
