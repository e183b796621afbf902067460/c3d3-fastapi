from fastapi import status, Request, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.cfg.settings import settings
from app.schemas.c3exposure.cex_open_order_screener.schema import (
    ExchangeTickerLabelORMSchema, NewAccountLimitOrderSchema
)
from app.services.router.service import RouterService as gateway


router = InferringRouter()


@cbv(router=router)
class CexOpenOrderScreenerCBV:

    @gateway.route(
        method=router.post,
        path='/new_cex_open_order',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_cex_open_order',
        service_url=settings.C3EXPOSURE_SERVICE_URL,
        response_model=ExchangeTickerLabelORMSchema,
        is_permission=True
    )
    async def on_post(self, request: Request, response: Response, new_cex_open_order: NewAccountLimitOrderSchema):
        pass
