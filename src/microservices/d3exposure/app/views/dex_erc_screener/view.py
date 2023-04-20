from fastapi import status, Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.services.dex_erc_screener.service import DexERCScreenerService
from app.schemas.dex_erc_screener.schema import (
    TokenOnWalletORMSchema, NewWalletBalancesSchema
)


router = InferringRouter()


@cbv(router=router)
class DexERCScreenerCBV:

    @router.post(path='/new_erc_screener', status_code=status.HTTP_201_CREATED, response_model=TokenOnWalletORMSchema)
    async def on_post(self, form: NewWalletBalancesSchema, service: DexERCScreenerService = Depends()):
        new_erc_screener = service.on_post(
            wallet_address=form.wallet_address,
            token_address=form.token_address,
            network_name=form.network_name,
            label_name=form.label_name
        )
        if not new_erc_screener:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chain not found."
            )
        return new_erc_screener
