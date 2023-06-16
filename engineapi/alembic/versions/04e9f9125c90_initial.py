"""Initial

Revision ID: 04e9f9125c90
Revises: 
Create Date: 2022-04-21 19:29:31.599594

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '04e9f9125c90'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dropper_contracts',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('blockchain', sa.VARCHAR(length=128), nullable=False),
    sa.Column('address', sa.VARCHAR(length=256), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', statement_timestamp())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', statement_timestamp())"), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_dropper_contracts')),
    sa.UniqueConstraint('blockchain', 'address', name=op.f('uq_dropper_contracts_blockchain')),
    sa.UniqueConstraint('id', name=op.f('uq_dropper_contracts_id'))
    )
    op.create_index(op.f('ix_dropper_contracts_address'), 'dropper_contracts', ['address'], unique=False)
    op.create_table('dropper_claims',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('dropper_contract_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('claim_id', sa.BigInteger(), nullable=True),
    sa.Column('title', sa.VARCHAR(length=128), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('terminus_address', sa.VARCHAR(length=256), nullable=False),
    sa.Column('terminus_pool_id', sa.BigInteger(), nullable=False),
    sa.Column('claim_block_deadline', sa.BigInteger(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', statement_timestamp())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', statement_timestamp())"), nullable=False),
    sa.ForeignKeyConstraint(['dropper_contract_id'], ['dropper_contracts.id'], name=op.f('fk_dropper_claims_dropper_contract_id_dropper_contracts'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_dropper_claims')),
    sa.UniqueConstraint('id', name=op.f('uq_dropper_claims_id'))
    )
    op.create_index(op.f('ix_dropper_claims_terminus_address'), 'dropper_claims', ['terminus_address'], unique=False)
    op.create_index(op.f('ix_dropper_claims_terminus_pool_id'), 'dropper_claims', ['terminus_pool_id'], unique=False)
    op.create_table('dropper_claimants',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('dropper_claim_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('address', sa.VARCHAR(length=256), nullable=False),
    sa.Column('amount', sa.BigInteger(), nullable=False),
    sa.Column('added_by', sa.VARCHAR(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', statement_timestamp())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', statement_timestamp())"), nullable=False),
    sa.ForeignKeyConstraint(['dropper_claim_id'], ['dropper_claims.id'], name=op.f('fk_dropper_claimants_dropper_claim_id_dropper_claims'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_dropper_claimants')),
    sa.UniqueConstraint('id', name=op.f('uq_dropper_claimants_id'))
    )
    op.create_index(op.f('ix_dropper_claimants_added_by'), 'dropper_claimants', ['added_by'], unique=False)
    op.create_index(op.f('ix_dropper_claimants_address'), 'dropper_claimants', ['address'], unique=False)
    # ### end Alembic commands ###

    # Manual
    op.execute("CREATE UNIQUE INDEX uq_dropper_claims_dropper_contract_id_claim_id ON dropper_claims(dropper_contract_id,claim_id) WHERE (claim_id is NOT NULL and active = true);")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dropper_claimants_address'), table_name='dropper_claimants')
    op.drop_index(op.f('ix_dropper_claimants_added_by'), table_name='dropper_claimants')
    op.drop_table('dropper_claimants')
    op.drop_index(op.f('ix_dropper_claims_terminus_pool_id'), table_name='dropper_claims')
    op.drop_index(op.f('ix_dropper_claims_terminus_address'), table_name='dropper_claims')
    op.drop_table('dropper_claims')
    op.drop_index(op.f('ix_dropper_contracts_address'), table_name='dropper_contracts')
    op.drop_table('dropper_contracts')
    # ### end Alembic commands ###

    # Manual
    op.execute("DROP INDEX uq_dropper_claims_dropper_contract_id_claim_id")