from fastapi import status, Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.services.dex_borrow_screener.service import DexBorrowScreenerService
from app.schemas.dex_borrow_screener.schema import (
    AddressChainProtocolSpecificationLabelORMSchema,
    NewHedgeToBorrowsSchema
)


router = InferringRouter()


@cbv(router=router)
class DexBorrowScreenerCBV:

    @router.post(path='/new_dex_borrow_screener', status_code=status.HTTP_201_CREATED, response_model=AddressChainProtocolSpecificationLabelORMSchema)
    async def on_post(self, form: NewHedgeToBorrowsSchema, service: DexBorrowScreenerService = Depends()):
        new_dex_borrow_screener = service.on_post(
            wallet_address=form.wallet_address,
            token_address=form.token_address,
            network_name=form.network_name,
            label_name=form.label_name,
            protocol_name=form.protocol_name,
            specification_name=form.specification_name
        )
        if not new_dex_borrow_screener:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chain not found."
            )
        return new_dex_borrow_screener
