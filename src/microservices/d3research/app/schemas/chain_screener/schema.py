from pydantic import BaseModel
from datetime import datetime


class NewChainSchema(BaseModel):
    network_name: str
    native_chain_token: str
    rpc_node: str
    block_limit: int
    network_uri: str
    network_api_key: str


class ChainORMSchema(BaseModel):
    h_chain_id: int

    h_network_name: str
    h_native_chain_token: str
    h_network_rpc_node: str
    h_network_block_limit: int
    h_network_uri: str
    h_network_api_key: str

    h_network_load_ts: datetime

    class Config:
        orm_mode = True
