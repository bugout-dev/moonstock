"""Additional indices

Revision ID: 2d967953f847
Revises: 1e33c3d07306
Create Date: 2021-07-29 14:27:44.624965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d967953f847'
down_revision = '1e33c3d07306'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_esd_event_signatures_id'), 'esd_event_signatures', ['id'], unique=False)
    op.create_index(op.f('ix_esd_function_signatures_id'), 'esd_function_signatures', ['id'], unique=False)
    op.create_index(op.f('ix_ethereum_blocks_hash'), 'ethereum_blocks', ['hash'], unique=False)
    op.create_unique_constraint(op.f('uq_ethereum_blocks_block_number'), 'ethereum_blocks', ['block_number'])
    op.create_index(op.f('ix_ethereum_pending_transactions_block_number'), 'ethereum_pending_transactions', ['block_number'], unique=False)
    op.create_index(op.f('ix_ethereum_pending_transactions_hash'), 'ethereum_pending_transactions', ['hash'], unique=True)
    op.create_index(op.f('ix_ethereum_pending_transactions_value'), 'ethereum_pending_transactions', ['value'], unique=False)
    op.create_index(op.f('ix_ethereum_transactions_block_number'), 'ethereum_transactions', ['block_number'], unique=False)
    op.create_index(op.f('ix_ethereum_transactions_hash'), 'ethereum_transactions', ['hash'], unique=True)
    op.create_index(op.f('ix_ethereum_transactions_value'), 'ethereum_transactions', ['value'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ethereum_transactions_value'), table_name='ethereum_transactions')
    op.drop_index(op.f('ix_ethereum_transactions_hash'), table_name='ethereum_transactions')
    op.drop_index(op.f('ix_ethereum_transactions_block_number'), table_name='ethereum_transactions')
    op.drop_index(op.f('ix_ethereum_pending_transactions_value'), table_name='ethereum_pending_transactions')
    op.drop_index(op.f('ix_ethereum_pending_transactions_hash'), table_name='ethereum_pending_transactions')
    op.drop_index(op.f('ix_ethereum_pending_transactions_block_number'), table_name='ethereum_pending_transactions')
    op.drop_constraint(op.f('uq_ethereum_blocks_block_number'), 'ethereum_blocks', type_='unique')
    op.drop_index(op.f('ix_ethereum_blocks_hash'), table_name='ethereum_blocks')
    op.drop_index(op.f('ix_esd_function_signatures_id'), table_name='esd_function_signatures')
    op.drop_index(op.f('ix_esd_event_signatures_id'), table_name='esd_event_signatures')
    # ### end Alembic commands ###
