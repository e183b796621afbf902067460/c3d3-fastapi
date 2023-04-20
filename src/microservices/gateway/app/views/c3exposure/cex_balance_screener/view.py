from fastapi import status, Request, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.cfg.settings import settings
from app.schemas.c3exposure.cex_balance_screener.schema import (
    ExchangeSymbolLabelORMSchema, NewAccountBalanceSchema
)
from app.services.router.service import RouterService as gateway


router = InferringRouter()


@cbv(router=router)
class CexBalanceScreenerCBV:

    @gateway.route(
        method=router.post,
        path='/new_cex_balance',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_cex_balance',
        service_url=settings.C3EXPOSURE_SERVICE_URL,
        response_model=ExchangeSymbolLabelORMSchema,
        is_permission=True
    )
    async def on_post(self, request: Request, response: Response, new_cex_balance: NewAccountBalanceSchema):
        pass
