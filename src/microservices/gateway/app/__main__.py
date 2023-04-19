from fastapi import FastAPI

from app.views.auth.view import app as auth_app
from app.views.с3research.router import app as c3research_app
from app.views.d3research.router import app as d3research_app
from app.views.warehouse.view import app as warehouse_app


app = FastAPI()

app.include_router(router=auth_app)
app.include_router(router=c3research_app)
app.include_router(router=d3research_app)
app.include_router(router=warehouse_app)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='view:app', host='0.0.0.0')
