from fastapi import status, Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.services.cex_liquidation_screener.service import CexLiquidationScreenerService
from app.schemas.cex_liquidation_screener.schema import (
    ExchangeTickerLabelORMSchema, NewAccountLiquidationSchema
)


router = InferringRouter()


@cbv(router=router)
class CexLiquidationScreenerCBV:

    @router.post(path='/new_cex_liquidation_screener', status_code=status.HTTP_201_CREATED, response_model=ExchangeTickerLabelORMSchema)
    async def on_post(self, form: NewAccountLiquidationSchema, service: CexLiquidationScreenerService = Depends()):
        new_cex_liquidation_screener = service.on_post(
            label_name=form.label_name,
            exchange_name=form.exchange_name,
            ticker_name=form.instrument_name
        )
        if not new_cex_liquidation_screener:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found."
            )
        return new_cex_liquidation_screener
