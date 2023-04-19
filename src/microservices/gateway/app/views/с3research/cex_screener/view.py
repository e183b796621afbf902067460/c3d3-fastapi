from fastapi import status, Request, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.cfg.settings import settings
from app.schemas.c3research.cex_screener.schema import (
    ExchangeTickerORMSchema, NewWholeMarketTradesHistory
)
from app.services.router.service import RouterService as gateway


router = InferringRouter()


@cbv(router=router)
class CexScreenerCBV:

    @gateway.route(
        method=router.post,
        path='/new_whole_market_trades_history',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_whole_market_trades_history',
        service_url=settings.C3RESEARCH_SERVICE_URL,
        response_model=ExchangeTickerORMSchema,
        is_permission=True
    )
    async def on_post(self, request: Request, response: Response, new_whole_market_trades_history: NewWholeMarketTradesHistory):
        pass
