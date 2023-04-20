from fastapi import FastAPI

from app.cfg.settings import settings
from app.views.cex_screener.view import router as cex_screener_router


app = FastAPI()


app.include_router(router=cex_screener_router, prefix=f'{settings.API_V1}' + f'{settings.SERVICE_ENDPOINT}' + '/cex_screener')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='__main__:app', host='0.0.0.0')
