import asyncio
import logging
from enum import Enum
from typing import Optional

from komoutils.core import KomoBase, safe_ensure_future
from pydantic import BaseModel

from aporacle.intervaled_data_symbol.client.orchestrator import Orchestrator


class AssetPriceData(BaseModel):
    chain: str
    epoch: int
    asset: str
    price: float


class Status(Enum):
    STARTED = "started"
    EPOCH_RUNNING = "epoch_running"
    EPOCH_COMPLETE = "epoch_complete"


class IntervaledTradingSymbolExecutor(KomoBase):

    def __init__(self,
                 symbol: str,
                 input_queue: asyncio.Queue,
                 output_record_evaluation_ticks: int = 18
                 ):
        super().__init__()
        self.symbol: str = symbol
        self.asset: str = self.symbol.split("_")[-2]
        self.input_queue: asyncio.Queue = input_queue
        self.output_record_evaluation_ticks = output_record_evaluation_ticks
        self.orchestrator: Optional[Orchestrator] = None
        self.chain: Optional[str] = None
        self.epoch: Optional[int] = None
        self.status: Optional[Status] = Status.STARTED
        self.results: dict = {"prices": None, "returns": None}

    @property
    def name(self):
        return "intervaled_trading_symbol_executor"

    def start(self, chain: str, epoch: int):
        self.chain = chain
        self.epoch = epoch

        self.orchestrator = Orchestrator(
            symbol=self.symbol,
            input_queue=self.input_queue,
            output_record_evaluation_ticks=self.output_record_evaluation_ticks,
        )
        self.orchestrator.start()
        self.status = Status.EPOCH_RUNNING

    def stop(self):
        pass

    def set_tso_data(self, asset_price_data: AssetPriceData):
        self.orchestrator.tso_price_set(chain=asset_price_data.chain,
                                        tso=asset_price_data.asset,
                                        price=asset_price_data.price)

    async def process(self):
        prices, returns = self.orchestrator.generate_chain_epoch_record(chain=self.chain, epoch=self.epoch)
        self.results["prices"] = prices.copy()
        self.results["returns"] = returns.copy()
        self.status = Status.EPOCH_COMPLETE
        self.log_with_clock(log_level=logging.INFO, msg=f"Epoch complete for {self.chain} {self.epoch}. ")



