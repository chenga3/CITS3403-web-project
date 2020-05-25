"""added problemscompleted

Revision ID: 57ef47d9904c
Revises: 2766ba754e10
Create Date: 2020-05-25 10:49:19.623425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57ef47d9904c'
down_revision = '2766ba754e10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('problems_completed',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('questionID', sa.Integer(), nullable=True),
    sa.Column('userID', sa.Integer(), nullable=True),
    sa.Column('success', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['questionID'], ['problem.id'], ),
    sa.ForeignKeyConstraint(['userID'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('problems_completed')
    # ### end Alembic commands ###
