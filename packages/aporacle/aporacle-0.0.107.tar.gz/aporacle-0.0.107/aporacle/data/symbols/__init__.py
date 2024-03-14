import pandas as pd
from cachetools import TTLCache, cached
from komoutils.core import KomoBase

from aporacle import MONGODB_URI, MONGODB_NAME
from aporacle.data.db.crud import Crud


class SymbolData(KomoBase):
    def __init__(self):
        self.crud: Crud = Crud(uri=MONGODB_URI, db_name=MONGODB_NAME)

    @cached(cache=TTLCache(maxsize=1024, ttl=3600))
    def get_symbol(self, symbol: str) -> list:
        filters = {"asset": symbol}
        return self.crud.read_symbol_data(filters)

    def get(self, symbol: str) -> pd.DataFrame:
        df = pd.DataFrame(self.get_symbol(symbol))
        return df
