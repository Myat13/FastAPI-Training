"""add foreign-key to posts table

Revision ID: 5a03bd5d3149
Revises: 93fe6f1c5927
Create Date: 2022-05-27 10:22:35.116950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a03bd5d3149'
down_revision = '93fe6f1c5927'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'post_user_fk', 
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE',
                         )
    pass


def downgrade():
    op.drop_constraint('post_user_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
