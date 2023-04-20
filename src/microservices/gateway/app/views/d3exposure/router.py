from fastapi_utils.inferring_router import APIRouter

from app.cfg.settings import settings
from app.views.d3exposure.chain_screener.view import router as chain_screener_router
from app.views.d3exposure.dex_borrow_screener.view import router as dex_borrow_screener_router
from app.views.d3exposure.dex_erc_screener.view import router as dex_erc_screener_router


app = APIRouter()

app.include_router(router=chain_screener_router, prefix=f'{settings.API_V1}' + f'{settings.D3EXPOSURE_SERVICE_ENDPOINT}' + '/chain_screener')
app.include_router(router=dex_borrow_screener_router, prefix=f'{settings.API_V1}' + f'{settings.D3EXPOSURE_SERVICE_ENDPOINT}' + '/dex_borrow_screener')
app.include_router(router=dex_erc_screener_router, prefix=f'{settings.API_V1}' + f'{settings.D3EXPOSURE_SERVICE_ENDPOINT}' + '/dex_erc_screener')
