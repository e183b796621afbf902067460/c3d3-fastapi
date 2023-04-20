from fastapi import status, Request, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.cfg.settings import settings
from app.schemas.c3exposure.account_screener.schema import (
    LabelORMSchema, NewLabelSchema
)
from app.services.router.service import RouterService as gateway


router = InferringRouter()


@cbv(router=router)
class AccountScreenerCBV:

    @gateway.route(
        method=router.post,
        path='/new_account',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_account',
        service_url=settings.C3EXPOSURE_SERVICE_URL,
        response_model=LabelORMSchema,
        is_permission=True
    )
    async def on_post(self, request: Request, response: Response, new_account: NewLabelSchema):
        pass
