"""add content column to posts table

Revision ID: 65ee4b11e56e
Revises: 63360f096224
Create Date: 2022-05-27 09:56:49.138738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65ee4b11e56e'
down_revision = '63360f096224'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content',)
    pass
