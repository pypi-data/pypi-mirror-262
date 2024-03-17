import asyncio
import enum
import logging
from collections import OrderedDict

import pendulum
import schedule
from komoutils.core import KomoBase
from komoutils.core.time import the_time_in_iso_now_is

from aporacle.intervaled_data_symbol.client.shared_data import SharedData
from aporacle.intervaled_data_symbol.client.tick import Tick


class CursorStatus(enum.Enum):
    STARTED = "STARTED"
    STOPPED = "STOPPED"
    PENDING = "PENDING"


class Cursor(KomoBase):

    def __init__(self, symbol: str):
        self.symbol: str = symbol
        self.tso: str = str(symbol).split("_")[2]
        self.quote: str = str(symbol).split("_")[3]
        self.ticks: OrderedDict = OrderedDict()

        self.status: CursorStatus = CursorStatus.PENDING

    def evaluation_ticks(self, age: int = 15) -> OrderedDict[str, Tick]:
        new_ticks = OrderedDict()
        for tick in self.ticks.values():
            if tick.age < age and tick.finalized is True:
                new_ticks[tick.stamp] = tick

        return new_ticks

    async def start(self):
        self.log_with_clock(log_level=logging.INFO, msg=f"Starting cursor for {self.symbol}. ")
        self.generator()
        # self.status = CursorStatus.STARTED
        schedule.every(5).seconds.do(self.generator)
        schedule.every(60).seconds.do(self.destroyer)
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)
            if self.status == CursorStatus.PENDING:
                self.log_with_clock(log_level=logging.INFO,
                                    msg=f"Cursor for {self.symbol} has a status of {self.status.value}. ")
            continue

    def generator(self):
        stamp = int(pendulum.now().timestamp())
        for s in range(stamp, stamp + 15, 1):
            if s in self.ticks:
                continue

            self.ticks[s] = Tick(symbol=self.symbol, stamp=s)

        finalized = [t for t in self.ticks.values() if t.finalized]
        self.log_with_clock(log_level=logging.INFO, msg=f"{len(finalized)} of {len(self.ticks)} of ticks for "
                                                        f"{self.symbol} have been finalized. ")

    def destroyer(self):
        candidates = [stamp for stamp, tick in self.ticks.items() if tick.expires_at < pendulum.now().timestamp()]
        for stamp in candidates:
            self.ticks.pop(stamp)

        self.log_with_clock(log_level=logging.INFO, msg=f"Destroyed {len(candidates)} ticks for {self.symbol} at "
                                                        f"{the_time_in_iso_now_is()}. ")

    def finalizer(self, stamp: int):
        try:
            # print(self.status)
            if self.status != CursorStatus.STARTED:
                return

            if len(self.ticks) == 0:
                self.log_with_clock(log_level=logging.WARNING, msg=f"No ticks available for {self.symbol}. ")

            assert stamp in self.ticks, f"Stamp error on {self.symbol}. "

            # print(f"Finalizing {stamp} at {the_time_in_iso_now_is()}.")

            sorted_dict = dict(sorted(self.ticks.items())).copy()
            means = [tick.mean for tick in sorted_dict.values() if tick.age < 120 and tick.finalized is True]
            returns: dict = {"flare": [], "songbird": []}
            try:
                for chain in ['flare', 'songbird']:
                    returns[chain] = [tick.returns[chain]
                                      for tick in sorted_dict.values()
                                      if tick.age < 120 and tick.finalized is True and tick.returns[chain] is not None]
            except Exception as e:
                pass

            # for tick in sorted_dict.values():
            #     print(f"{tick.stamp} {tick.returns}")


            # print(means)
            self.ticks[stamp].finalize_prices(previous_price_means=means)
            self.ticks[stamp].finalize_returns(previous_returns_means=returns)

            SharedData.get_instance().last_close = self.ticks[stamp].close
            SharedData.get_instance().last_returns = self.ticks[stamp].returns
            # self.ticks[stamp + 1].initialize(previous_close=self.ticks[stamp].close,
            #                                  previous_returns=self.ticks[stamp].returns)

        except AssertionError as ae:
            self.log_with_clock(log_level=logging.ERROR, msg=f"{ae}")
        except Exception as e:
            raise
