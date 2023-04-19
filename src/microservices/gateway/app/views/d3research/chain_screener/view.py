from fastapi import status, Request, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.cfg.settings import settings
from app.schemas.d3research.chain_screener.schema import (
    NewChainSchema, ChainORMSchema
)
from app.services.router.service import RouterService as gateway


router = InferringRouter()


@cbv(router=router)
class ChainScreenerCBV:

    @gateway.route(
        method=router.post,
        path='/new_chain',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_chain',
        service_url=settings.D3RESEARCH_SERVICE_URL,
        response_model=ChainORMSchema,
        is_permission=True
    )
    async def on_post(self, request: Request, response: Response, new_chain: NewChainSchema):
        pass
