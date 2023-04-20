from pydantic import BaseModel
from datetime import datetime


class ExchangeTickerLabelORMSchema(BaseModel):
    l_exchange_ticker_label_id: int
    h_label_id: int
    l_exchange_ticker_id: int
    l_exchange_ticker_label_load_ts: datetime

    class Config:
        orm_mode = True


class NewAccountLiquidationSchema(BaseModel):
    label_name: str
    exchange_name: str
    instrument_name: str
