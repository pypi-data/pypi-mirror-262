from typing import List, Optional

import pandas as pd
from komoutils.core import KomoBase

from aporacle.data.asset import AssetData
from aporacle.data.symbols import SymbolData


class Combination(KomoBase):
    def __init__(self, symbols: List[str] = None):
        self.symbols: Optional[list] = symbols
        self.combined: Optional[pd.DataFrame] = None
        self.symbol_data: SymbolData = SymbolData()
        self.asset_data: AssetData = AssetData()

    def combine(self, data: List[pd.DataFrame]):
        self.combined = pd.concat(data, axis=1)
        return self.combined

    def get(self):
        data: List[pd.DataFrame] = [self.symbol_data.get(symbol) for symbol in self.symbols]
        return self.combine(data)
