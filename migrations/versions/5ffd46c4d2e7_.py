"""empty message

Revision ID: 5ffd46c4d2e7
Revises: 8e909e5a7833, 77dd3be075b9, ab53010b516f
Create Date: 2020-05-25 11:55:03.291546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ffd46c4d2e7'
down_revision = ('8e909e5a7833', '77dd3be075b9', 'ab53010b516f')
branch_labels = None
depends_on = None


def upgrade():
    print("test")
    pass


def downgrade():
    pass
