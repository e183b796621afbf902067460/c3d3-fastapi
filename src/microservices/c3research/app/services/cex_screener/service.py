from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Optional
from cryptography import fernet

from app.schemas.cex_screener.schema import (
    ExchangeTickerORMSchema
)
from app.orm.cfg.engine import ORMSettings
from app.cfg.settings import settings
from app.orm import base


class CexScreenerService:

    def __init__(self, session: Session = Depends(ORMSettings.get_session)):
        self._session: Session = session
        self._fn = fernet.Fernet(key=settings.JWT_FERNET_KEY)

    def _get_h_exchange_by_name(self, exchange_name: str) -> Optional[base.hExchanges]:
        return self._session.query(base.hExchanges).filter_by(h_exchange_name=exchange_name).first()

    def _get_h_ticker_by_name(self, ticker_name: str) -> Optional[base.hTickers]:
        return self._session.query(base.hTickers).filter_by(h_ticker_name=ticker_name).first()

    def _get_l_exchange_ticker(self, exchange_name: str, ticker_name: str) -> Optional[base.lExchangesTickers]:
        h_exchange, h_ticker = self._get_h_exchange_by_name(exchange_name=exchange_name), self._get_h_ticker_by_name(ticker_name=ticker_name)
        if not h_exchange or not h_ticker:
            return None
        return self._session.query(base.lExchangesTickers).filter_by(
            h_exchange_id=h_exchange.h_exchange_id,
            h_ticker_id=h_ticker.h_ticker_id
        ).first()

    def _insert_h_exchange(self, exchange_name: str) -> base.hExchanges:
        h_exchange = self._get_h_exchange_by_name(exchange_name=exchange_name)
        if not h_exchange:
            h_exchange = base.hExchanges(
                h_exchange_name=exchange_name
            )
            self._session.add(h_exchange)
            self._session.commit()
        return h_exchange

    def _insert_h_ticker(self, ticker_name: str) -> base.hTickers:
        h_ticker = self._get_h_ticker_by_name(ticker_name=ticker_name)
        if not h_ticker:
            h_ticker = base.hTickers(
                h_ticker_name=ticker_name
            )
            self._session.add(h_ticker)
            self._session.commit()
        return h_ticker

    def _insert_l_exchange_ticker(self, exchange_name: str, ticker_name: str) -> base.lExchangesTickers:
        h_exchange, h_ticker = self._insert_h_exchange(exchange_name=exchange_name), self._insert_h_ticker(ticker_name=ticker_name)

        l_exchange_ticker = self._get_l_exchange_ticker(exchange_name=h_exchange.h_exchange_name, ticker_name=h_ticker.h_ticker_name)
        if not l_exchange_ticker:
            l_exchange_ticker = base.lExchangesTickers(
                h_exchange_id=h_exchange.h_exchange_id,
                h_ticker_id=h_ticker.h_ticker_id
            )
            self._session.add(l_exchange_ticker)
            self._session.commit()
        return l_exchange_ticker

    def _hash_by_fernet(self, value: str) -> str:
        return self._fn.encrypt(value.encode()).decode()

    def on_post(self, exchange_name: str, ticker_name: str) -> ExchangeTickerORMSchema:
        l_exchange_ticker = self._insert_l_exchange_ticker(
            exchange_name=exchange_name,
            ticker_name=ticker_name
        )
        return ExchangeTickerORMSchema.from_orm(l_exchange_ticker)
