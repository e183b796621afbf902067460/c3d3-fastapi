from fastapi import status, Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.services.cex_open_order_screener.service import CexOpenOrderScreenerService
from app.schemas.cex_open_order_screener.schema import (
    ExchangeTickerLabelORMSchema, NewAccountLimitOrderSchema
)


router = InferringRouter()


@cbv(router=router)
class CexOpenOrderScreenerCBV:

    @router.post(path='/new_cex_open_order', status_code=status.HTTP_201_CREATED, response_model=ExchangeTickerLabelORMSchema)
    async def on_post(self, form: NewAccountLimitOrderSchema, service: CexOpenOrderScreenerService = Depends()):
        new_cex_open_order = service.on_post(
            label_name=form.label_name,
            exchange_name=form.exchange_name,
            ticker_name=form.instrument_name
        )
        if not new_cex_open_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found."
            )
        return new_cex_open_order
