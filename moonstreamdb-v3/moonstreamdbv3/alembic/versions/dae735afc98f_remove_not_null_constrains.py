"""Remove not null constrains

Revision ID: dae735afc98f
Revises: e6d3c285e7cc
Create Date: 2025-01-05 16:28:54.796023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dae735afc98f'
down_revision: Union[str, None] = 'e6d3c285e7cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('amoy_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('amoy_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('amoy_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('arbitrum_nova_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('arbitrum_nova_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('arbitrum_nova_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('arbitrum_one_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('arbitrum_one_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('arbitrum_one_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('arbitrum_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('arbitrum_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('arbitrum_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('avalanche_fuji_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('avalanche_fuji_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('avalanche_fuji_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('avalanche_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('avalanche_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('avalanche_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('b3_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('b3_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('b3_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('b3_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('b3_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('b3_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('base_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('base_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('base_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('blast_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('blast_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('blast_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('blast_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('blast_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('blast_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('ethereum_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('ethereum_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('ethereum_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('game7_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('game7_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('game7_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('game7_orbit_arbitrum_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('game7_orbit_arbitrum_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('game7_orbit_arbitrum_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('game7_testnet_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('game7_testnet_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('game7_testnet_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('imx_zkevm_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('imx_zkevm_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('imx_zkevm_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('imx_zkevm_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('imx_zkevm_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('imx_zkevm_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('mantle_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('mantle_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('mantle_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('mantle_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('mantle_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('mantle_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('mumbai_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('mumbai_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('mumbai_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('polygon_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('polygon_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('polygon_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('proofofplay_apex_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('proofofplay_apex_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('proofofplay_apex_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('ronin_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('ronin_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('ronin_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('ronin_saigon_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('ronin_saigon_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('ronin_saigon_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('starknet_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('starknet_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('starknet_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('starknet_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('starknet_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('starknet_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('xai_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('xai_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('xai_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('xai_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('xai_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('xai_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('xdai_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('xdai_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('xdai_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('zksync_era_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('zksync_era_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('zksync_era_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('zksync_era_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('zksync_era_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('zksync_era_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.alter_column('zksync_era_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('zksync_era_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('zksync_era_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('zksync_era_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('zksync_era_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('zksync_era_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('xdai_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('xdai_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('xdai_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('xai_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('xai_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('xai_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('xai_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('xai_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('xai_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('starknet_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('starknet_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('starknet_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('starknet_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('starknet_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('starknet_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('ronin_saigon_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('ronin_saigon_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('ronin_saigon_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('ronin_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('ronin_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('ronin_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('proofofplay_apex_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('proofofplay_apex_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('proofofplay_apex_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('polygon_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('polygon_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('polygon_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('mumbai_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('mumbai_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('mumbai_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('mantle_sepolia_labels', 'address',
               existing_type=postgresql.BYTEA(),
               nullable=True)
    op.alter_column('mantle_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('mantle_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('mantle_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('mantle_labels', 'address',
               existing_type=postgresql.BYTEA(),
               nullable=True)
    op.alter_column('mantle_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('mantle_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('mantle_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('imx_zkevm_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('imx_zkevm_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('imx_zkevm_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('imx_zkevm_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('imx_zkevm_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('imx_zkevm_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('game7_testnet_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('game7_testnet_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('game7_testnet_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('game7_orbit_arbitrum_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('game7_orbit_arbitrum_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('game7_orbit_arbitrum_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('game7_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('game7_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('game7_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('ethereum_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('ethereum_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('ethereum_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('blast_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('blast_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('blast_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('blast_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('blast_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('blast_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('base_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('base_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('base_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('b3_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('b3_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('b3_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('b3_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('b3_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('b3_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('avalanche_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('avalanche_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('avalanche_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('avalanche_fuji_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('avalanche_fuji_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('avalanche_fuji_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('arbitrum_sepolia_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('arbitrum_sepolia_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('arbitrum_sepolia_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('arbitrum_one_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('arbitrum_one_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('arbitrum_one_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('arbitrum_nova_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('arbitrum_nova_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('arbitrum_nova_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('amoy_labels', 'block_timestamp',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('amoy_labels', 'block_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('amoy_labels', 'transaction_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###
