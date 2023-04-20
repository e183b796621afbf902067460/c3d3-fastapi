from pydantic import BaseModel
from datetime import datetime


class NewWalletBalancesSchema(BaseModel):
    wallet_address: str
    token_address: str
    network_name: str
    label_name: str


class TokenOnWalletORMSchema(BaseModel):
    l_token_on_wallet_id: int
    l_address_chain_id: int
    l_address_chain_label_id: int
    l_token_on_wallet_load_ts: datetime

    class Config:
        orm_mode = True
