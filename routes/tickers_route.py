import pandas as pd
import yfinance as yf
from fastapi import APIRouter
from joblib import Parallel, delayed

from data.tickers_data import TickerInfoList, TickerList
from tools.cache import session
from tools.const import VALID_INVESTORS_COLUMN_COUNT

router = APIRouter(prefix="/tickers", tags=["tickers"])


def process_ticker_info(ticker_name: str, ticker_data: yf.Ticker, period: str, interval: str) -> dict:
    institutional_holders = ticker_data.institutional_holders
    if (isinstance(institutional_holders, pd.DataFrame)
            and len(institutional_holders.columns) == VALID_INVESTORS_COLUMN_COUNT):
        institutional_holders = institutional_holders.to_dict(orient="records")
    else:
        institutional_holders = []

    quotes = ticker_data.history(
        period=period,
        interval=interval,
    ).reset_index().to_dict(orient="records")

    return {
        "ticker": ticker_name,
        "quotes": quotes,
        "institutional_holders": institutional_holders,
    }


@router.post("/info")
async def ticker_info(tickers_list: TickerList) -> TickerInfoList:
    response = Parallel(n_jobs=-1, prefer="threads")(
        delayed(process_ticker_info)(
            ticker_name, ticker_data, tickers_list.period, tickers_list.interval
        )
        for ticker_name, ticker_data in yf.Tickers(
            tickers_list.tickers, session=session
        ).tickers.items()
    )

    return response


@router.get("/options/{ticker_name}")
async def has_trading_options(ticker_name: str) -> bool:
    ticker = yf.Ticker(ticker_name)

    return len(ticker.options) > 0
