from fastapi import status, Request, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.cfg.settings import settings
from app.schemas.c3exposure.cex_liquidation_screener.schema import (
    ExchangeTickerLabelORMSchema, NewAccountLiquidationSchema
)
from app.services.router.service import RouterService as gateway


router = InferringRouter()


@cbv(router=router)
class CexLiquidationScreenerCBV:

    @gateway.route(
        method=router.post,
        path='/new_cex_liquidation_screener',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_cex_liquidation_screener',
        service_url=settings.C3EXPOSURE_SERVICE_URL,
        response_model=ExchangeTickerLabelORMSchema,
        is_permission=True
    )
    async def on_post(self, request: Request, response: Response, new_cex_liquidation_screener: NewAccountLiquidationSchema):
        pass
