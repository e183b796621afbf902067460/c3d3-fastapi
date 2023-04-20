from pydantic import BaseModel
from datetime import datetime


class AddressChainProtocolSpecificationLabelORMSchema(BaseModel):
    l_address_chain_protocol_specification_label_id: int
    l_address_chain_label_id: int
    l_address_chain_protocol_specification_id: int
    l_address_chain_protocol_specification_label_load_ts: datetime

    class Config:
        orm_mode = True


class NewHedgeToBorrowsSchema(BaseModel):
    wallet_address: str
    token_address: str
    network_name: str
    label_name: str
    protocol_name: str
    specification_name: str
