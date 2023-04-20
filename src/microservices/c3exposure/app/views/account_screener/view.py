from fastapi import status, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.services.account_screener.service import AccountScreenerService
from app.schemas.account_screener.schema import (
    LabelORMSchema, NewLabelSchema
)


router = InferringRouter()


@cbv(router=router)
class AccountScreenerCBV:

    @router.post(path='/new_account', status_code=status.HTTP_201_CREATED, response_model=LabelORMSchema)
    async def on_post(self, form: NewLabelSchema, service: AccountScreenerService = Depends()):
        new_account = service.on_post(
            label_name=form.label_name,
            label_api_key=form.label_api_key,
            label_api_secret=form.label_api_secret
        )
        return new_account
