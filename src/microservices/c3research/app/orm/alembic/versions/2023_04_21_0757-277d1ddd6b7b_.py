"""empty message

Revision ID: 277d1ddd6b7b
Revises: 
Create Date: 2023-04-21 07:57:47.495913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '277d1ddd6b7b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('h_exchanges',
    sa.Column('h_exchange_id', sa.Integer(), nullable=False),
    sa.Column('h_exchange_name', sa.Text(), nullable=False),
    sa.Column('h_exchange_load_ts', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('h_exchange_id'),
    sa.UniqueConstraint('h_exchange_name')
    )
    op.create_table('h_tickers',
    sa.Column('h_ticker_id', sa.Integer(), nullable=False),
    sa.Column('h_ticker_name', sa.Text(), nullable=False),
    sa.Column('h_ticker_load_ts', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('h_ticker_id'),
    sa.UniqueConstraint('h_ticker_name')
    )
    op.create_table('l_exchanges_tickers',
    sa.Column('l_exchange_ticker_id', sa.Integer(), nullable=False),
    sa.Column('h_exchange_id', sa.Integer(), nullable=False),
    sa.Column('h_ticker_id', sa.Integer(), nullable=False),
    sa.Column('l_exchange_ticker_load_ts', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['h_exchange_id'], ['h_exchanges.h_exchange_id'], ),
    sa.ForeignKeyConstraint(['h_ticker_id'], ['h_tickers.h_ticker_id'], ),
    sa.PrimaryKeyConstraint('l_exchange_ticker_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('l_exchanges_tickers')
    op.drop_table('h_tickers')
    op.drop_table('h_exchanges')
    # ### end Alembic commands ###
