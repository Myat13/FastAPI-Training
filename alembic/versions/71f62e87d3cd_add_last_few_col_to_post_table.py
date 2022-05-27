"""add last few col to post table

Revision ID: 71f62e87d3cd
Revises: 5a03bd5d3149
Create Date: 2022-05-27 10:30:47.825215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71f62e87d3cd'
down_revision = '5a03bd5d3149'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), 
        nullable=False, 
        server_default='TRUE'
    ))
    
    op.add_column('posts', sa.Column(
        'created_at', 
        sa.TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=sa.text('NOW()'),
    ))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
