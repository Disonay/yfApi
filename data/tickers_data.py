from pandas import Timestamp
from pydantic import BaseModel, Field, conlist, validator

from tools.const import (
    MAX_TICKETS_NUMBER,
    MIN_TICKETS_NUMBER,
    VALID_INTERVALS,
    VALID_PERIODS,
    TICKERS_EXAMPLE,
    PERIOD_EXAMPLE,
    INVTERVAL_EXAMPLE,
)


class TickerList(BaseModel):
    tickers: list[str] = Field(example=TICKERS_EXAMPLE)
    period: str = Field(example=PERIOD_EXAMPLE, description="Possible values " + " ".join(VALID_PERIODS))
    interval: str = Field(example=INVTERVAL_EXAMPLE, description="Possible values " + " ".join(VALID_INTERVALS))

    @validator("tickers")
    def tickers_count(cls, v):
        if not MIN_TICKETS_NUMBER <= len(v) <= MAX_TICKETS_NUMBER:
            raise ValueError("The number of tickets must be from 1 to 1000")

        return v

    @validator("period")
    def period_possible_values(cls, v):
        if v not in VALID_PERIODS:
            raise ValueError("Valid periods: " + " ".join(VALID_PERIODS))

        return v

    @validator("interval")
    def interval_possible_values(cls, v):
        if v not in VALID_INTERVALS:
            raise ValueError("Valid intervals: " + " ".join(VALID_INTERVALS))

        return v


class Quote(BaseModel):
    date: Timestamp = Field(None, alias="Date")
    open: int = Field(None, alias="Open")
    close: int = Field(None, alias="Close")
    high: int = Field(None, alias="High")
    low: int = Field(None, alias="Low")
    volume: int = Field(None, alias="Volume")
    dividends: int = Field(None, alias="Dividends")
    stock: int = Field(None, alias="Stock Splits")


class InstitutionalHolder(BaseModel):
    holder: str = Field(None, alias="Holder")
    shares: int = Field(None, alias="Shares")
    date_reported: Timestamp = Field(None, alias="Date Reported")
    out: float = Field(None, alias="% Out")
    value: int = Field(None, alias="Value")


class TickerInfo(BaseModel):
    ticker: str
    quotes: conlist(Quote, min_items=0)
    institutional_holders: conlist(InstitutionalHolder, min_items=0)


class TickerInfoList(BaseModel):
    __root__: list[TickerInfo]
