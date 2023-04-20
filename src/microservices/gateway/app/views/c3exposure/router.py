from fastapi_utils.inferring_router import APIRouter

from app.cfg.settings import settings
from app.views.c3exposure.account_screener.view import router as account_screener_router
from app.views.c3exposure.cex_balance_screener.view import router as cex_balance_screener_router
from app.views.c3exposure.cex_liquidation_screener.view import router as cex_liquidation_screener_router
from app.views.c3exposure.cex_open_order_screener.view import router as cex_open_order_screener_router


app = APIRouter()

app.include_router(router=account_screener_router, prefix=f'{settings.API_V1}' + f'{settings.C3EXPOSURE_SERVICE_ENDPOINT}' + '/account_screener')
app.include_router(router=cex_balance_screener_router, prefix=f'{settings.API_V1}' + f'{settings.C3EXPOSURE_SERVICE_ENDPOINT}' + '/cex_balance_screener')
app.include_router(router=cex_liquidation_screener_router, prefix=f'{settings.API_V1}' + f'{settings.C3EXPOSURE_SERVICE_ENDPOINT}' + '/cex_liquidation_screener')
app.include_router(router=cex_open_order_screener_router, prefix=f'{settings.API_V1}' + f'{settings.C3EXPOSURE_SERVICE_ENDPOINT}' + '/cex_open_order_screener')
