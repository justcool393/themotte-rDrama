
"""make body and body_html for comment and submission infinite

Revision ID: f60e66d3372d
Revises: ba8a214736eb
Create Date: 2023-02-17 02:16:47.436983+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f60e66d3372d'
down_revision = 'ba8a214736eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'body_html',
               existing_type=sa.VARCHAR(length=40000),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'body_html',
               existing_type=sa.VARCHAR(length=40000),
               nullable=True)
    # ### end Alembic commands ###
