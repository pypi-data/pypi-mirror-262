import asyncio
import logging
import time
from collections import OrderedDict
from typing import Optional

from aporacle.intervaled_data_symbol.client.symbol import Symbol
from aporacle.intervaled_data_symbol.client.tick import Tick


class IntervaledSymbol(Symbol):
    def __init__(self,
                 symbol: str,
                 input_trading_data_queue: asyncio.Queue,
                 output_record_evaluation_ticks: int = 15):
        super().__init__(symbol, input_trading_data_queue)
        self.output_record_evaluation_ticks = output_record_evaluation_ticks
        self.evaluation_ticks: Optional[OrderedDict[str, Tick]] = None

    def create_prices_output_record(self, chain: str, epoch: int):
        prices = {"chain": chain, "epoch": epoch, "symbol": self.symbol, "asset": self.asset, "type": "chain_epoch_prices"}
        for index, tick in enumerate(reversed(self.evaluation_ticks.values())):
            prices.update(tick.get_prices(index=index))

        sma_ticks = list(reversed(self.evaluation_ticks.values()))[0:5]
        for index, tick in enumerate(sma_ticks):
            prices.update(tick.get_prices_smas(index=index))

        return prices

    def create_returns_output_record(self, chain: str, epoch: int):
        returns = {"chain": chain, "epoch": epoch, "symbol": self.symbol, "asset": self.asset, "type": "chain_epoch_returns"}

        for index, tick in enumerate(reversed(self.evaluation_ticks.values())):
            returns.update(tick.get_returns(chain=chain, index=index))

        sma_ticks = list(reversed(self.evaluation_ticks.values()))[0:5]
        for index, tick in enumerate(sma_ticks):
            returns.update(tick.get_returns_smas(chain=chain, index=index))

        return returns

    def run(self, chain: str, epoch: int):
        try:
            t1 = time.perf_counter()
            self.evaluation_ticks = self.cursor.evaluation_ticks(age=self.output_record_evaluation_ticks)
            prices = self.create_prices_output_record(chain=chain, epoch=epoch)
            returns = self.create_returns_output_record(chain=chain, epoch=epoch)
            t2 = time.perf_counter()
            self.log_with_clock(log_level=logging.DEBUG, msg=f"Chain {chain} epoch {epoch} took {t2 - t1} seconds. ")
            return prices, returns
        except Exception as e:
            return 'failure'
