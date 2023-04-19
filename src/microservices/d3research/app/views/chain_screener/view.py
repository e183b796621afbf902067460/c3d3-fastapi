from fastapi import status, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.services.chain_screener.service import ChainScreenerService
from app.schemas.chain_screener.schema import (
    ChainORMSchema, NewChainSchema
)


router = InferringRouter()


@cbv(router=router)
class ChainScreenerCBV:

    @router.post(path='/new_chain', status_code=status.HTTP_201_CREATED, response_model=ChainORMSchema)
    async def on_post(self, form: NewChainSchema, service: ChainScreenerService = Depends()):
        new_chain = service.on_post(
            network_name=form.network_name,
            native_chain_token=form.native_chain_token,
            rpc_node=form.rpc_node,
            block_limit=form.block_limit,
            network_uri=form.network_uri,
            network_api_key=form.network_api_key
        )
        return new_chain
