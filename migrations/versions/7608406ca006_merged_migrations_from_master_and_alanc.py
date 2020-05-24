"""merged migrations from master and alanc

Revision ID: 7608406ca006
Revises: 48c3ed01cb03, e0a08acdaad7
Create Date: 2020-05-24 11:05:19.431198

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7608406ca006'
down_revision = ('48c3ed01cb03', 'e0a08acdaad7')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
