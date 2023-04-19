from fastapi import FastAPI

from app.cfg.settings import settings
from app.views.chain_screener.view import router as chain_screener_router
from app.views.dex_screener.view import router as dex_screener_router


app = FastAPI()


app.include_router(router=chain_screener_router, prefix=f'{settings.API_V1}' + f'{settings.SERVICE_ENDPOINT}' + '/chain_screener')
app.include_router(router=dex_screener_router, prefix=f'{settings.API_V1}' + f'{settings.SERVICE_ENDPOINT}' + '/dex_screener')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='view:app', host='0.0.0.0')
