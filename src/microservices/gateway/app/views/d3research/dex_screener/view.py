from fastapi import status, Request, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.cfg.settings import settings
from app.schemas.d3research.dex_screener.schema import (
    AddressChainProtocolSpecificationORMSchema, NewLiquidityPoolSchema
)
from app.services.router.service import RouterService as gateway


router = InferringRouter()


@cbv(router=router)
class DexScreenerCBV:

    @gateway.route(
        method=router.post,
        path='/new_liquidity_pool',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_liquidity_pool',
        service_url=settings.D3RESEARCH_SERVICE_URL,
        response_model=AddressChainProtocolSpecificationORMSchema,
        is_permission=True
    )
    async def on_post(self, request: Request, response: Response, new_liquidity_pool: NewLiquidityPoolSchema):
        pass
