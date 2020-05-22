"""added user lang preference

Revision ID: e0a08acdaad7
Revises: 1b6e10c5a8d3
Create Date: 2020-05-22 10:34:05.488766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0a08acdaad7'
down_revision = '1b6e10c5a8d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_problem_difficulty'), 'problem', ['difficulty'], unique=False)
    op.add_column('user', sa.Column('prefer_language', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'prefer_language')
    op.drop_index(op.f('ix_problem_difficulty'), table_name='problem')
    # ### end Alembic commands ###
