from fastapi import FastAPI

from app.cfg.settings import settings
from app.views.account_screener.view import router as account_screener_router
from app.views.cex_balance_screener.view import router as cex_balance_screener
from app.views.cex_liquidation_screener.view import router as cex_liquidation_screener
from app.views.cex_open_order_screener.view import router as cex_open_order_screener


app = FastAPI()


app.include_router(router=account_screener_router, prefix=f'{settings.API_V1}' + f'{settings.SERVICE_ENDPOINT}' + '/account_screener')
app.include_router(router=cex_balance_screener, prefix=f'{settings.API_V1}' + f'{settings.SERVICE_ENDPOINT}' + '/cex_balance_screener')
app.include_router(router=cex_liquidation_screener, prefix=f'{settings.API_V1}' + f'{settings.SERVICE_ENDPOINT}' + '/cex_liquidation_screener')
app.include_router(router=cex_open_order_screener, prefix=f'{settings.API_V1}' + f'{settings.SERVICE_ENDPOINT}' + '/cex_open_order_screener')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='__main__:app', host='0.0.0.0')
