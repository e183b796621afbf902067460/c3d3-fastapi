from fastapi import status, Request, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.cfg.settings import settings
from app.schemas.d3exposure.dex_erc_screener.schema import (
    NewWalletBalancesSchema, TokenOnWalletORMSchema
)
from app.services.router.service import RouterService as gateway


router = InferringRouter()


@cbv(router=router)
class DexERCScreenerCBV:

    @gateway.route(
        method=router.post,
        path='/new_erc_screener',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_erc_screener',
        service_url=settings.D3EXPOSURE_SERVICE_URL,
        response_model=TokenOnWalletORMSchema,
        is_permission=True
    )
    async def on_post(self, request: Request, response: Response, new_erc_screener: NewWalletBalancesSchema):
        pass
