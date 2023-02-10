from abc import ABC

import yfinance as yf
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket


class CachedLimiterSession(CacheMixin, LimiterMixin, Session, ABC):
    pass


session = CachedLimiterSession(
    per_second=0.9,
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache"),
)

yf.set_tz_cache_location("/cache/location")
