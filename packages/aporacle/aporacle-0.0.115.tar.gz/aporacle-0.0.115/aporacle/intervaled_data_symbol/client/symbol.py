import asyncio
import logging

import pendulum
from komoutils.core import safe_ensure_future, KomoBase

from aporacle.intervaled_data_symbol.client.cursor import Cursor, CursorStatus
from aporacle.intervaled_data_symbol.client.shared_data import SharedData
from aporacle.intervaled_data_symbol.client.tick import Tick
from aporacle.intervaled_data_symbol.client.trades import Trades


class Symbol(KomoBase):

    def __init__(self, symbol: str, input_trading_data_queue: asyncio.Queue):
        self.symbol = symbol
        self.input_trading_data_queue: asyncio.Queue = input_trading_data_queue

        self.asset = str(self.symbol).split("_")[2]
        self.cursor: Cursor = Cursor(symbol=self.symbol)

    def start(self):
        safe_ensure_future(self.cursor.start())
        safe_ensure_future(self.trades_data_loop())

    async def trades_data_loop(self):
        self.log_with_clock(log_level=logging.INFO, msg=f"Started trades data loop for {self.symbol}. ")

        try:
            self.log_with_clock(log_level=logging.INFO, msg=f"Waiting for the first trade for {self.symbol}. ")
            while True:
                trade = await self.input_trading_data_queue.get()
                if 'type' not in trade:
                    continue

                if trade['type'] != 'trade':
                    continue

                if str(trade['base']).upper() != self.asset.upper():
                    continue

                # print(trade)
                if trade['symbol'] not in [self.symbol]:
                    continue

                if abs(pendulum.now().diff(pendulum.parse(trade['timestamp_at_exchange'])).in_seconds()) > 30:
                    continue

                # timestamp = int(pendulum.parse(trade['timestamp_at_exchange']).timestamp())
                timestamp = int(pendulum.parse(trade['timestamp_at_connector']).timestamp())
                if timestamp not in Trades.get_instance().trades:
                    Trades.get_instance().trades[timestamp] = []

                Trades.get_instance().trades[timestamp].append(trade)
                SharedData.get_instance().last_close = trade['price']

                # print(f"Status {self.cursor.status} {self.asset}".upper())
                if self.cursor.status == CursorStatus.PENDING:
                    self.cursor.status = CursorStatus.STARTED

                if timestamp not in self.cursor.ticks:
                    print(f"Creating Timestamp Not Available {timestamp} {trade['timestamp_at_exchange']} {self.symbol}".upper())
                    self.cursor.ticks[timestamp] = Tick(symbol=self.symbol, stamp=timestamp)

                self.input_trading_data_queue.task_done()
        except Exception as e:
            raise e
