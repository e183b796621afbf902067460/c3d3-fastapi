from fastapi import status, Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.services.dex_screener.service import DexScreenerService
from app.schemas.dex_screener.schema import (
    AddressChainProtocolSpecificationORMSchema, NewLiquidityPoolSchema
)


router = InferringRouter()


@cbv(router=router)
class DexScreenerCBV:

    @router.post(path='/new_liquidity_pool', status_code=status.HTTP_201_CREATED, response_model=AddressChainProtocolSpecificationORMSchema)
    async def on_post__new_bids_and_asks(self, form: NewLiquidityPoolSchema, service: DexScreenerService = Depends()):
        new_bids_and_asks = service.on_post(
            pool_address=form.pool_address,
            network_name=form.network_name,
            protocol_name=form.protocol_name,
            specification_name=form.specification_name,
            is_reverse=form.is_reverse
        )
        if not new_bids_and_asks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chain not found."
            )
        return new_bids_and_asks

