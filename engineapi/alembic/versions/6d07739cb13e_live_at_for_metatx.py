"""Live at for metatx

Revision ID: 6d07739cb13e
Revises: cc80e886e153
Create Date: 2023-12-06 14:33:04.814144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d07739cb13e'
down_revision = 'cc80e886e153'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('call_requests', sa.Column('live_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('call_requests', 'live_at')
    # ### end Alembic commands ###