from pydantic import BaseModel
from datetime import datetime


class NewLiquidityPoolSchema(BaseModel):
    pool_address: str
    network_name: str
    protocol_name: str
    specification_name: str
    is_reverse: bool


class AddressChainProtocolSpecificationORMSchema(BaseModel):
    l_address_chain_protocol_specification_id: int
    l_address_chain_id: int
    l_protocol_specification_id: int
    l_address_chain_protocol_specification_load_ts: datetime

    class Config:
        orm_mode = True
