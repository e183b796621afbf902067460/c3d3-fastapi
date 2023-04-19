from fastapi import status, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.services.cex_screener.service import CexScreenerService
from app.schemas.cex_screener.schema import (
    ExchangeTickerORMSchema, NewWholeMarketTradesHistory
)


router = InferringRouter()


@cbv(router=router)
class CexScreenerCBV:

    @router.post(path='/new_whole_market_trades_history', status_code=status.HTTP_201_CREATED, response_model=ExchangeTickerORMSchema)
    async def on_post(self, form: NewWholeMarketTradesHistory, service: CexScreenerService = Depends()):
        new_whole_market_trades_history = service.on_post(
            exchange_name=form.exchange_name,
            ticker_name=form.instrument_name
        )
        return new_whole_market_trades_history
