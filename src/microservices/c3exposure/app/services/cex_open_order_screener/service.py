from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Optional
from cryptography import fernet

from app.schemas.cex_open_order_screener.schema import (
    ExchangeTickerLabelORMSchema
)
from app.orm.cfg.engine import ORMSettings
from app.cfg.settings import settings
from app.orm import base


class CexOpenOrderScreenerService:

    def __init__(self, session: Session = Depends(ORMSettings.get_session)):
        self._session: Session = session
        self._fn = fernet.Fernet(key=settings.JWT_FERNET_KEY)

    def _get_h_exchange_by_name(self, exchange_name: str) -> Optional[base.hExchanges]:
        return self._session.query(base.hExchanges).filter_by(h_exchange_name=exchange_name).first()

    def _get_h_label_by_name(self, label_name: str) -> Optional[base.hLabels]:
        return self._session.query(base.hLabels).filter_by(h_label_name=label_name).first()

    def _get_h_ticker_by_name(self, ticker_name: str) -> Optional[base.hTickers]:
        return self._session.query(base.hTickers).filter_by(h_ticker_name=ticker_name).first()

    def _get_h_symbol_by_name(self, symbol_name: str) -> Optional[base.hSymbols]:
        return self._session.query(base.hSymbols).filter_by(h_symbol_name=symbol_name).first()

    def _get_l_exchange_ticker(self, exchange_name: str, ticker_name: str) -> Optional[base.lExchangesTickers]:
        h_exchange, h_ticker = self._get_h_exchange_by_name(exchange_name=exchange_name), self._get_h_ticker_by_name(ticker_name=ticker_name)
        if not h_exchange or not h_ticker:
            return None
        return self._session.query(base.lExchangesTickers).filter_by(
            h_exchange_id=h_exchange.h_exchange_id,
            h_ticker_id=h_ticker.h_ticker_id
        ).first()

    def _get_l_exchange_ticker_label(self, exchange_name: str, ticker_name: str, label_name: str) -> Optional[base.lExchangesTickersLabels]:
        l_exchange_ticker, h_label = self._get_l_exchange_ticker(exchange_name=exchange_name, ticker_name=ticker_name), self._get_h_label_by_name(label_name=label_name)
        if not l_exchange_ticker or not h_label:
            return None
        return self._session.query(base.lExchangesTickersLabels).filter_by(
            l_exchange_ticker_id=l_exchange_ticker.l_exchange_ticker_id,
            h_label_id=h_label.h_label_id
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

    def _insert_l_exchange_ticker_label(self, exchange_name: str, ticker_name: str, label_name: str) -> Optional[base.lExchangesTickersLabels]:
        h_exchange, h_ticker, h_label = self._insert_h_exchange(
            exchange_name=exchange_name
        ), self._insert_h_ticker(
            ticker_name=ticker_name
        ), self._get_h_label_by_name(label_name=label_name)

        if not h_label:
            return None

        l_exchange_ticker_label = self._get_l_exchange_ticker_label(exchange_name=h_exchange.h_exchange_name, ticker_name=h_ticker.h_ticker_name, label_name=h_label.h_label_name)
        if not l_exchange_ticker_label:
            l_exchange_ticker = self._insert_l_exchange_ticker(exchange_name=h_exchange.h_exchange_name, ticker_name=h_ticker.h_ticker_name)

            l_exchange_ticker_label = base.lExchangesTickersLabels(
                h_label_id=h_label.h_label_id,
                l_exchange_ticker_id=l_exchange_ticker.l_exchange_ticker_id
            )
            self._session.add(l_exchange_ticker_label)
            self._session.commit()
        return l_exchange_ticker_label

    def on_post(self, label_name: str, exchange_name: str, ticker_name: str) -> Optional[ExchangeTickerLabelORMSchema]:
        l_exchange_ticker_label = self._insert_l_exchange_ticker_label(
            exchange_name=exchange_name,
            ticker_name=ticker_name,
            label_name=label_name
        )
        return ExchangeTickerLabelORMSchema.from_orm(l_exchange_ticker_label) if l_exchange_ticker_label else None
