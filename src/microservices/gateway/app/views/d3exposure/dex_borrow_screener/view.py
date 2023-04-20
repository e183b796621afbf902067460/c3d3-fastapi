from fastapi import status, Request, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.cfg.settings import settings
from app.schemas.d3exposure.dex_borrow_screener.schema import (
    NewHedgeToBorrowsSchema, AddressChainProtocolSpecificationLabelORMSchema
)
from app.services.router.service import RouterService as gateway


router = InferringRouter()


@cbv(router=router)
class DexBorrowScreenerCBV:

    @gateway.route(
        method=router.post,
        path='/new_dex_borrow_screener',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_dex_borrow_screener',
        service_url=settings.D3EXPOSURE_SERVICE_URL,
        response_model=AddressChainProtocolSpecificationLabelORMSchema,
        is_permission=True
    )
    async def on_post(self, request: Request, response: Response, new_dex_borrow_screener: NewHedgeToBorrowsSchema):
        pass
