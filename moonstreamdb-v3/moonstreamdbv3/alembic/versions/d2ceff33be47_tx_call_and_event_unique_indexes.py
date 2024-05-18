"""tx call and event unique indexes

Revision ID: d2ceff33be47
Revises: e9f640a2b45b
Create Date: 2024-05-17 16:35:56.059519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2ceff33be47'
down_revision: Union[str, None] = 'e9f640a2b45b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('uk_amoy_labels_transaction_hash_log_index_event', 'amoy_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_amoy_labels_transaction_hash_tx_call', 'amoy_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_amoy_labels_id'), 'amoy_labels', ['id'])
    op.create_index('uk_arbitrum_nova_labels_transaction_hash_log_index_event', 'arbitrum_nova_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_arbitrum_nova_labels_transaction_hash_tx_call', 'arbitrum_nova_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_arbitrum_nova_labels_id'), 'arbitrum_nova_labels', ['id'])
    op.create_index('uk_arbitrum_one_labels_transaction_hash_log_index_event', 'arbitrum_one_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_arbitrum_one_labels_transaction_hash_tx_call', 'arbitrum_one_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_arbitrum_one_labels_id'), 'arbitrum_one_labels', ['id'])
    op.create_index('ix_arbitrum_sepolia_labels_addr_block_ts', 'arbitrum_sepolia_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index('uk_arbitrum_sepolia_labels_transaction_hash_log_index_event', 'arbitrum_sepolia_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_arbitrum_sepolia_labels_transaction_hash_tx_call', 'arbitrum_sepolia_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_arbitrum_sepolia_labels_id'), 'arbitrum_sepolia_labels', ['id'])
    op.create_index('ix_avalanche_fuji_labels_addr_block_ts', 'avalanche_fuji_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index('uk_avalanche_fuji_labels_transaction_hash_log_index_event', 'avalanche_fuji_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_avalanche_fuji_labels_transaction_hash_tx_call', 'avalanche_fuji_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_avalanche_fuji_labels_id'), 'avalanche_fuji_labels', ['id'])
    op.create_index('ix_avalanche_labels_addr_block_ts', 'avalanche_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index('uk_avalanche_labels_transaction_hash_log_index_event', 'avalanche_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_avalanche_labels_transaction_hash_tx_call', 'avalanche_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_avalanche_labels_id'), 'avalanche_labels', ['id'])
    op.create_index('ix_base_labels_addr_block_ts', 'base_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index('uk_base_labels_transaction_hash_log_index_event', 'base_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_base_labels_transaction_hash_tx_call', 'base_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_base_labels_id'), 'base_labels', ['id'])
    op.create_index('uk_blast_labels_transaction_hash_log_index_event', 'blast_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_blast_labels_transaction_hash_tx_call', 'blast_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_blast_labels_id'), 'blast_labels', ['id'])
    op.create_index('uk_blast_sepolia_labels_transaction_hash_log_index_event', 'blast_sepolia_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_blast_sepolia_labels_transaction_hash_tx_call', 'blast_sepolia_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_blast_sepolia_labels_id'), 'blast_sepolia_labels', ['id'])
    op.create_index('ix_ethereum_labels_addr_block_ts', 'ethereum_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index('uk_ethereum_labels_transaction_hash_log_index_event', 'ethereum_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_ethereum_labels_transaction_hash_tx_call', 'ethereum_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_ethereum_labels_id'), 'ethereum_labels', ['id'])
    op.create_index('ix_mumbai_labels_addr_block_ts', 'mumbai_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index('uk_mumbai_labels_transaction_hash_log_index_event', 'mumbai_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_mumbai_labels_transaction_hash_tx_call', 'mumbai_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_mumbai_labels_id'), 'mumbai_labels', ['id'])
    op.create_index('ix_polygon_labels_addr_block_ts', 'polygon_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index('uk_polygon_labels_transaction_hash_log_index_event', 'polygon_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_polygon_labels_transaction_hash_tx_call', 'polygon_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_polygon_labels_id'), 'polygon_labels', ['id'])
    op.create_index('uk_proofofplay_apex_labels_transaction_hash_log_index_event', 'proofofplay_apex_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_proofofplay_apex_labels_transaction_hash_tx_call', 'proofofplay_apex_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_proofofplay_apex_labels_id'), 'proofofplay_apex_labels', ['id'])
    op.create_index('ix_sepolia_labels_addr_block_ts', 'sepolia_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index('uk_sepolia_labels_transaction_hash_log_index_event', 'sepolia_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_sepolia_labels_transaction_hash_tx_call', 'sepolia_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_sepolia_labels_id'), 'sepolia_labels', ['id'])
    op.create_index('ix_starknet_labels_addr_block_ts', 'starknet_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index('uk_starknet_labels_transaction_hash_log_index_event', 'starknet_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_starknet_labels_transaction_hash_tx_call', 'starknet_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_starknet_labels_id'), 'starknet_labels', ['id'])
    op.create_index('ix_starknet_sepolia_labels_addr_block_ts', 'starknet_sepolia_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index('uk_starknet_sepolia_labels_transaction_hash_log_index_event', 'starknet_sepolia_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_starknet_sepolia_labels_transaction_hash_tx_call', 'starknet_sepolia_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_starknet_sepolia_labels_id'), 'starknet_sepolia_labels', ['id'])
    op.create_index('ix_xai_labels_addr_block_ts', 'xai_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index('uk_xai_labels_transaction_hash_log_index_event', 'xai_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_xai_labels_transaction_hash_tx_call', 'xai_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_xai_labels_id'), 'xai_labels', ['id'])
    op.create_index('ix_xai_sepolia_labels_addr_block_ts', 'xai_sepolia_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index('uk_xai_sepolia_labels_transaction_hash_log_index_event', 'xai_sepolia_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_xai_sepolia_labels_transaction_hash_tx_call', 'xai_sepolia_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_xai_sepolia_labels_id'), 'xai_sepolia_labels', ['id'])
    op.create_index('ix_xdai_labels_addr_block_ts', 'xdai_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index('uk_xdai_labels_transaction_hash_log_index_event', 'xdai_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_xdai_labels_transaction_hash_tx_call', 'xdai_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_xdai_labels_id'), 'xdai_labels', ['id'])
    op.create_index('ix_zksync_era_labels_addr_block_ts', 'zksync_era_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index('uk_zksync_era_labels_transaction_hash_log_index_event', 'zksync_era_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_zksync_era_labels_transaction_hash_tx_call', 'zksync_era_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_zksync_era_labels_id'), 'zksync_era_labels', ['id'])
    op.create_index('ix_zksync_era_sepolia_labels_addr_block_ts', 'zksync_era_sepolia_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index('uk_zksync_era_sepolia_labels_transaction_hash_log_index_event', 'zksync_era_sepolia_labels', ['transaction_hash', 'log_index'], unique=True, postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.create_index('uk_zksync_era_sepolia_labels_transaction_hash_tx_call', 'zksync_era_sepolia_labels', ['transaction_hash'], unique=True, postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.create_unique_constraint(op.f('uq_zksync_era_sepolia_labels_id'), 'zksync_era_sepolia_labels', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_zksync_era_sepolia_labels_id'), 'zksync_era_sepolia_labels', type_='unique')
    op.drop_index('uk_zksync_era_sepolia_labels_transaction_hash_tx_call', table_name='zksync_era_sepolia_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_zksync_era_sepolia_labels_transaction_hash_log_index_event', table_name='zksync_era_sepolia_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index('ix_zksync_era_sepolia_labels_addr_block_ts', table_name='zksync_era_sepolia_labels')
    op.drop_constraint(op.f('uq_zksync_era_labels_id'), 'zksync_era_labels', type_='unique')
    op.drop_index('uk_zksync_era_labels_transaction_hash_tx_call', table_name='zksync_era_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_zksync_era_labels_transaction_hash_log_index_event', table_name='zksync_era_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index('ix_zksync_era_labels_addr_block_ts', table_name='zksync_era_labels')
    op.drop_constraint(op.f('uq_xdai_labels_id'), 'xdai_labels', type_='unique')
    op.drop_index('uk_xdai_labels_transaction_hash_tx_call', table_name='xdai_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_xdai_labels_transaction_hash_log_index_event', table_name='xdai_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index('ix_xdai_labels_addr_block_ts', table_name='xdai_labels')
    op.drop_constraint(op.f('uq_xai_sepolia_labels_id'), 'xai_sepolia_labels', type_='unique')
    op.drop_index('uk_xai_sepolia_labels_transaction_hash_tx_call', table_name='xai_sepolia_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_xai_sepolia_labels_transaction_hash_log_index_event', table_name='xai_sepolia_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index('ix_xai_sepolia_labels_addr_block_ts', table_name='xai_sepolia_labels')
    op.drop_constraint(op.f('uq_xai_labels_id'), 'xai_labels', type_='unique')
    op.drop_index('uk_xai_labels_transaction_hash_tx_call', table_name='xai_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_xai_labels_transaction_hash_log_index_event', table_name='xai_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index('ix_xai_labels_addr_block_ts', table_name='xai_labels')
    op.drop_constraint(op.f('uq_starknet_sepolia_labels_id'), 'starknet_sepolia_labels', type_='unique')
    op.drop_index('uk_starknet_sepolia_labels_transaction_hash_tx_call', table_name='starknet_sepolia_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_starknet_sepolia_labels_transaction_hash_log_index_event', table_name='starknet_sepolia_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index('ix_starknet_sepolia_labels_addr_block_ts', table_name='starknet_sepolia_labels')
    op.drop_constraint(op.f('uq_starknet_labels_id'), 'starknet_labels', type_='unique')
    op.drop_index('uk_starknet_labels_transaction_hash_tx_call', table_name='starknet_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_starknet_labels_transaction_hash_log_index_event', table_name='starknet_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index('ix_starknet_labels_addr_block_ts', table_name='starknet_labels')
    op.drop_constraint(op.f('uq_sepolia_labels_id'), 'sepolia_labels', type_='unique')
    op.drop_index('uk_sepolia_labels_transaction_hash_tx_call', table_name='sepolia_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_sepolia_labels_transaction_hash_log_index_event', table_name='sepolia_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index('ix_sepolia_labels_addr_block_ts', table_name='sepolia_labels')
    op.drop_constraint(op.f('uq_proofofplay_apex_labels_id'), 'proofofplay_apex_labels', type_='unique')
    op.drop_index('uk_proofofplay_apex_labels_transaction_hash_tx_call', table_name='proofofplay_apex_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_proofofplay_apex_labels_transaction_hash_log_index_event', table_name='proofofplay_apex_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_constraint(op.f('uq_polygon_labels_id'), 'polygon_labels', type_='unique')
    op.drop_index('uk_polygon_labels_transaction_hash_tx_call', table_name='polygon_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_polygon_labels_transaction_hash_log_index_event', table_name='polygon_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index('ix_polygon_labels_addr_block_ts', table_name='polygon_labels')
    op.drop_constraint(op.f('uq_mumbai_labels_id'), 'mumbai_labels', type_='unique')
    op.drop_index('uk_mumbai_labels_transaction_hash_tx_call', table_name='mumbai_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_mumbai_labels_transaction_hash_log_index_event', table_name='mumbai_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index('ix_mumbai_labels_addr_block_ts', table_name='mumbai_labels')
    op.drop_constraint(op.f('uq_ethereum_labels_id'), 'ethereum_labels', type_='unique')
    op.drop_index('uk_ethereum_labels_transaction_hash_tx_call', table_name='ethereum_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_ethereum_labels_transaction_hash_log_index_event', table_name='ethereum_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index('ix_ethereum_labels_addr_block_ts', table_name='ethereum_labels')
    op.drop_constraint(op.f('uq_blast_sepolia_labels_id'), 'blast_sepolia_labels', type_='unique')
    op.drop_index('uk_blast_sepolia_labels_transaction_hash_tx_call', table_name='blast_sepolia_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_blast_sepolia_labels_transaction_hash_log_index_event', table_name='blast_sepolia_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_constraint(op.f('uq_blast_labels_id'), 'blast_labels', type_='unique')
    op.drop_index('uk_blast_labels_transaction_hash_tx_call', table_name='blast_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_blast_labels_transaction_hash_log_index_event', table_name='blast_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_constraint(op.f('uq_base_labels_id'), 'base_labels', type_='unique')
    op.drop_index('uk_base_labels_transaction_hash_tx_call', table_name='base_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_base_labels_transaction_hash_log_index_event', table_name='base_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index('ix_base_labels_addr_block_ts', table_name='base_labels')
    op.drop_constraint(op.f('uq_avalanche_labels_id'), 'avalanche_labels', type_='unique')
    op.drop_index('uk_avalanche_labels_transaction_hash_tx_call', table_name='avalanche_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_avalanche_labels_transaction_hash_log_index_event', table_name='avalanche_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index('ix_avalanche_labels_addr_block_ts', table_name='avalanche_labels')
    op.drop_constraint(op.f('uq_avalanche_fuji_labels_id'), 'avalanche_fuji_labels', type_='unique')
    op.drop_index('uk_avalanche_fuji_labels_transaction_hash_tx_call', table_name='avalanche_fuji_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_avalanche_fuji_labels_transaction_hash_log_index_event', table_name='avalanche_fuji_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index('ix_avalanche_fuji_labels_addr_block_ts', table_name='avalanche_fuji_labels')
    op.drop_constraint(op.f('uq_arbitrum_sepolia_labels_id'), 'arbitrum_sepolia_labels', type_='unique')
    op.drop_index('uk_arbitrum_sepolia_labels_transaction_hash_tx_call', table_name='arbitrum_sepolia_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_arbitrum_sepolia_labels_transaction_hash_log_index_event', table_name='arbitrum_sepolia_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_index('ix_arbitrum_sepolia_labels_addr_block_ts', table_name='arbitrum_sepolia_labels')
    op.drop_constraint(op.f('uq_arbitrum_one_labels_id'), 'arbitrum_one_labels', type_='unique')
    op.drop_index('uk_arbitrum_one_labels_transaction_hash_tx_call', table_name='arbitrum_one_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_arbitrum_one_labels_transaction_hash_log_index_event', table_name='arbitrum_one_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_constraint(op.f('uq_arbitrum_nova_labels_id'), 'arbitrum_nova_labels', type_='unique')
    op.drop_index('uk_arbitrum_nova_labels_transaction_hash_tx_call', table_name='arbitrum_nova_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_arbitrum_nova_labels_transaction_hash_log_index_event', table_name='arbitrum_nova_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    op.drop_constraint(op.f('uq_amoy_labels_id'), 'amoy_labels', type_='unique')
    op.drop_index('uk_amoy_labels_transaction_hash_tx_call', table_name='amoy_labels', postgresql_where=sa.text("label='seer' and label_type='tx_call'"))
    op.drop_index('uk_amoy_labels_transaction_hash_log_index_event', table_name='amoy_labels', postgresql_where=sa.text("label='seer' and label_type='event'"))
    # ### end Alembic commands ###
