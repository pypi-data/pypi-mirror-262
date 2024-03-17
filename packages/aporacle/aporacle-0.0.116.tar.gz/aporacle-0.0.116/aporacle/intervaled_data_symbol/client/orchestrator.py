import asyncio
import logging
from typing import Optional, Tuple

import pendulum
import schedule
from komoutils.core import KomoBase, safe_ensure_future

from aporacle.intervaled_data_symbol.client.cursor import Cursor
from aporacle.intervaled_data_symbol.client.intervaled_symbol import IntervaledSymbol
from aporacle.intervaled_data_symbol.client.shared_data import SharedData


class Finalizer(KomoBase):

    def __init__(self, cursor: Cursor):
        self.cursor: Cursor = cursor
        schedule.every(1).seconds.do(self.run)

    async def start(self):
        self.log_with_clock(log_level=logging.INFO, msg=f"Initializing orchestrator summarizer. ")
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)
            continue

    def run(self):
        self.cursor.finalizer(stamp=int(pendulum.now().subtract(seconds=2).timestamp()))


class Orchestrator(KomoBase):

    def __init__(self,
                 symbol: str,
                 input_queue: asyncio.Queue,
                 output_record_evaluation_ticks: int = 18
                 ):
        self.symbol: str = symbol
        self.input_queue: asyncio.Queue = input_queue
        self.output_record_evaluation_ticks = output_record_evaluation_ticks

        self.intervaled: Optional[IntervaledSymbol] = None
        self.finalizer: Optional[Finalizer] = None

        self.initialize()

    def initialize(self):
        self.intervaled = IntervaledSymbol(symbol=self.symbol,
                                           input_trading_data_queue=self.input_queue,
                                           output_record_evaluation_ticks=self.output_record_evaluation_ticks)
        self.finalizer = Finalizer(cursor=self.intervaled.cursor)

    def start(self):
        self.intervaled.start()
        safe_ensure_future(self.finalizer.start())

    def tso_price_set(self, chain: str, tso: str, price: float):
        if self.symbol.split("_")[-2] not in [tso]:
            self.log_with_clock(log_level=logging.WARNING, msg=f"Incorrect TSO for price set. Tried to set {tso} but "
                                                               f"{self.symbol.split('_')[-2]} is allowable. ")
            return

        SharedData.get_instance().current_tso_prices[chain] = {tso: price}

    def generate_chain_epoch_record(self, chain: str, epoch: int) -> Tuple[dict, dict]:
        return self.intervaled.run(chain=chain, epoch=epoch)

