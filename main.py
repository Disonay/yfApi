from fastapi import FastAPI

from routes import tickers_route

app = FastAPI()

app.include_router(tickers_route.router)


@app.get("/health")
async def root() -> bool:
    return True
