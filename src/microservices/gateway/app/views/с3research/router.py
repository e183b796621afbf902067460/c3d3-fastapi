from fastapi_utils.inferring_router import APIRouter

from app.views.с3research.cex_screener.view import router as cex_screener_router
from app.cfg.settings import settings


app = APIRouter()

app.include_router(router=cex_screener_router, prefix=f'{settings.API_V1}' + f'{settings.C3RESEARCH_SERVICE_ENDPOINT}' + '/cex_screener')
