from fastapi_utils.inferring_router import APIRouter

from app.cfg.settings import settings
from app.views.d3research.dex_screener.view import router as dex_screener_router
from app.views.d3research.chain_screener.view import router as chain_screener_router


app = APIRouter()

app.include_router(router=dex_screener_router, prefix=f'{settings.API_V1}' + f'{settings.D3RESEARCH_SERVICE_ENDPOINT}' + '/dex_screener')
app.include_router(router=chain_screener_router, prefix=f'{settings.API_V1}' + f'{settings.D3RESEARCH_SERVICE_ENDPOINT}' + '/chain_screener')
