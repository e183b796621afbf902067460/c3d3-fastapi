from pydantic import BaseModel
from datetime import datetime


class ExchangeSymbolLabelORMSchema(BaseModel):
    l_exchange_symbol_label_id: int
    h_label_id: int
    l_exchange_symbol_id: int
    l_exchange_symbol_label_load_ts: datetime

    class Config:
        orm_mode = True


class NewAccountBalanceSchema(BaseModel):
    exchange_name: str
    instrument_name: str
    label_name: str
