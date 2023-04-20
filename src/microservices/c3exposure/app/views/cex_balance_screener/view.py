from fastapi import status, Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.services.cex_balance_screener.service import CexBalanceScreenerService
from app.schemas.cex_balance_screener.schema import (
    ExchangeSymbolLabelORMSchema, NewAccountBalanceSchema
)


router = InferringRouter()


@cbv(router=router)
class CexBalanceScreenerCBV:

    @router.post(path='/new_cex_balance', status_code=status.HTTP_201_CREATED, response_model=ExchangeSymbolLabelORMSchema)
    async def on_post(self, form: NewAccountBalanceSchema, service: CexBalanceScreenerService = Depends()):
        new_cex_balance = service.on_post(
            label_name=form.label_name,
            exchange_name=form.exchange_name,
            symbol_name=form.instrument_name
        )
        if not new_cex_balance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found."
            )
        return new_cex_balance
