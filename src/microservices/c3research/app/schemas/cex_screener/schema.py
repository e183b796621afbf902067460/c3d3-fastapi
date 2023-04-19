from pydantic import BaseModel
from datetime import datetime


class ExchangeTickerORMSchema(BaseModel):
    l_exchange_ticker_id: int
    h_exchange_id: int
    h_ticker_id: int
    l_exchange_ticker_load_ts: datetime

    class Config:
        orm_mode = True


class NewWholeMarketTradesHistory(BaseModel):
    exchange_name: str
    instrument_name: str
