from fastapi import FastAPI

from routes import tickers_route

app = FastAPI()

app.include_router(tickers_route.router)


@app.get("/")
async def root():
    return {"Python API to get some information about companies traded on the exchange"}
