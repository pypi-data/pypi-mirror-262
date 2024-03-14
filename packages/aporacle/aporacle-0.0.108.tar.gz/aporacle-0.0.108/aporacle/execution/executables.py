import asyncio
import json
import logging
import os
from typing import Optional

import websockets
from komoutils.core import KomoBase, safe_ensure_future
from komoutils.core.time import give_me_time_in_iso


class ChainEpochExecutable(KomoBase):
    def __init__(self, chain_tso_ws_endpoints: dict, schedule_source_keys: list):
        super().__init__()

        self.chain_tso_ws_endpoints: dict = chain_tso_ws_endpoints
        self.schedule_source_keys: list = schedule_source_keys
        self.chain_epoch_interval: int = os.getenv("CHAIN_EPOCH_INTERVAL", 90)
        self.end_time_execution_buffer: int = os.getenv("END_TIME_EXECUTION_BUFFER", 20)

        self._schedule_queue: asyncio.Queue = asyncio.Queue()
        self.epoch_schedule: Optional[dict] = {"flare": None, "songbird": None}

        self._epoch_scheduler_task: Optional[asyncio.Task] = None
        self._ws_listener_task: Optional[asyncio.Task] = None

        self._ready: bool = False

    @property
    def name(self):
        return "chain_epoch_executable"

    def initialize(self):
        raise NotImplementedError

    async def start(self):
        await self.initialize()
        self._epoch_scheduler_task = safe_ensure_future(self.epoch_scheduling_loop())
        [safe_ensure_future(self.tso_listener_loop(chain=chain)) for chain in self.chain_tso_ws_endpoints.keys()]
        self._ready = True

    def stop(self):
        pass

    def chain_tso_message_processor(self, message: dict):
        raise NotImplementedError

    def epoch_schedule_processor(self, message: dict):
        raise NotImplementedError

    async def epoch_scheduling_loop(self):
        # Connect to the server as listener
        while True:
            self.log_with_clock(log_level=logging.INFO,
                                msg=f"Awaiting the next schedule message, "
                                    f"from {self.schedule_source_keys}")
            interval_adjusted_start_time = self.chain_epoch_interval + self.end_time_execution_buffer
            message = await self._schedule_queue.get()
            if "chain" not in message:
                self.log_with_clock(log_level=logging.ERROR, msg=f"Received message with no chain assignment. "
                                                                 f"Message will be ignored. ")
                continue

            # Avoid duplicate scheduling. Will be useful in deployments where multiple/redundant schedulers are used.
            
            if message["epoch"] <= self.epoch_schedule[message["chain"]]["epoch"]:
                self.log_with_clock(log_level=logging.WARNING,
                                    msg=f"Epoch {message['chain']} for chain {message['epoch']} "
                                        f"has already been scheduled. ")
                continue

            self.log_with_clock(log_level=logging.INFO, msg=f"{message}")
            self.log_with_clock(log_level=logging.INFO,
                                msg=f"Epoch Start {give_me_time_in_iso(timestamp=message['end_time'] - interval_adjusted_start_time, short=True)} \n"
                                    f"Epoch End {give_me_time_in_iso(timestamp=message['end_time'], short=True)}")
            self.epoch_schedule[message["chain"]] = {
                "epoch": message['epoch'],
                "chain": message["chain"],
                "start_time": message["end_time"] - self.chain_epoch_interval,
                "end_time": message["end_time"],
                "st_str": give_me_time_in_iso(message["end_time"] - interval_adjusted_start_time),
                "et_str": give_me_time_in_iso(message["end_time"])
            }

            self.epoch_schedule_processor(message=self.epoch_schedule[message["chain"]])

    async def tso_listener_loop(self, chain: str):

        self.log_with_clock(log_level=logging.INFO, msg=f"Establishing a connection to TSO data at "
                                                        f"{self.chain_tso_ws_endpoints[chain]}. ")

        try:
            async with websockets.connect(f"ws://{self.chain_tso_ws_endpoints[chain]}") as websocket:
                self.log_with_clock(log_level=logging.INFO,
                                    msg=f"Connection to {self.chain_tso_ws_endpoints[chain]} for "
                                        f"TSO data is now active. ")
                while True:
                    try:
                        data = await websocket.recv()
                        message = json.loads(data)
                        if message["type"] in self.schedule_source_keys:
                            self.log_with_clock(log_level=logging.INFO,
                                                msg=f"Got new schedule message for epoch {message['epoch']}. ")

                            safe_ensure_future(self._schedule_queue.put(message))
                            self.log_with_clock(log_level=logging.INFO,
                                                msg=f"Waiting for the next TSO schedule message, "
                                                    f"from {self.schedule_source_keys}. ")

                            continue

                        self.chain_tso_message_processor(message=message)

                    except websockets.ConnectionClosed as cc:
                        self.log_with_clock(log_level=logging.ERROR,
                                            msg=f"Connection to {self.chain_tso_ws_endpoints[chain]} "
                                                f"was closed. {cc}. Will try to re-establish connection. ")
                        await asyncio.sleep(1)
                        safe_ensure_future(self.tso_listener_loop(chain=chain))
                        break

        except Exception as e:
            self.log_with_clock(log_level=logging.ERROR,
                                msg=f"Failed to connect to {self.chain_tso_ws_endpoints[chain]}. "
                                    f"On message - {e}. Will try again in 10 seconds. ")
            safe_ensure_future(self.tso_listener_loop(chain=chain))
            raise e
