from fastapi import FastAPI

from app.cfg.settings import settings
from app.views.chain_screener.view import router as chain_screener_router
from app.views.dex_borrow_screener.view import router as dex_borrow_screener_router
from app.views.dex_erc_screener.view import router as dex_erc_screener_router


app = FastAPI()


app.include_router(router=chain_screener_router, prefix=f'{settings.API_V1}' + f'{settings.SERVICE_ENDPOINT}' + '/chain_screener')
app.include_router(router=dex_borrow_screener_router, prefix=f'{settings.API_V1}' + f'{settings.SERVICE_ENDPOINT}' + '/dex_borrow_screener')
app.include_router(router=dex_erc_screener_router, prefix=f'{settings.API_V1}' + f'{settings.SERVICE_ENDPOINT}' + '/dex_erc_screener')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='view:app', host='0.0.0.0')
