import uvicorn
from fastapi import FastAPI
from db import database
from the_flask_and_fastapi_framework.dz.dz_6_dop_vozm_fastapi import routers_models

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(routers_models.router, tags=["DZ_6"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
