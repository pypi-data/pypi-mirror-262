import asyncio
import json
import logging
import os
from typing import Optional

import websockets
from komoutils.core import KomoBase, safe_ensure_future

from aporacle import conf


class VotingRoundExecutable(KomoBase):
    def __init__(self, chain_tso_ws_endpoints: dict, schedule_source_keys: list):
        super().__init__()

        self.schedule_source_keys: list = schedule_source_keys

        self._schedule_queue: asyncio.Queue = asyncio.Queue()
        self.epoch_schedule: Optional[dict] = {"coston": None, "flare": None, "songbird": None}

        self._epoch_scheduler_task: Optional[asyncio.Task] = None
        self._ws_listener_task: Optional[asyncio.Task] = None

        self._ready: bool = False

    @property
    def name(self):
        return "voting_round_executable"

    def initialize(self):
        raise NotImplementedError

    async def start(self):
        await self.initialize()
        self._epoch_scheduler_task = safe_ensure_future(self.epoch_scheduling_loop())
        [safe_ensure_future(self.tso_listener_loop(chain=chain)) for chain in self.epoch_schedule.keys()]
        self._ready = True

    def stop(self):
        pass

    def utilities_message_processor(self, message: dict):
        raise NotImplementedError

    def epoch_schedule_processor(self, message: dict):
        raise NotImplementedError

    async def epoch_scheduling_loop(self):
        # Connect to the server as listener
        while True:
            self.log_with_clock(log_level=logging.INFO,
                                msg=f"Awaiting the next schedule message, "
                                    f"from {self.schedule_source_keys}")
            message = await self._schedule_queue.get()
            if "chain" not in message:
                self.log_with_clock(log_level=logging.ERROR, msg=f"Received message with no chain assignment. "
                                                                 f"Message will be ignored. ")
                continue

            # Avoid duplicate scheduling. Will be useful in deployments where multiple/redundant schedulers are used.
            
            if message["voting_round"] <= self.epoch_schedule[message["chain"]]["voting_round"]:
                self.log_with_clock(log_level=logging.WARNING,
                                    msg=f"Voting round {message['voting_round']} for chain {message['chain']} "
                                        f"has already been scheduled. ")
                continue

            self.epoch_schedule[message["chain"]] = {
                "chain": message["chain"],
                "reward_epoch": message['reward_epoch'],
                "voting_round": message['voting_round'],
                "start_time": message["voting_round_start"],
            }

            self.epoch_schedule_processor(message=self.epoch_schedule[message["chain"]])

    async def tso_listener_loop(self, chain: str):
        url = f"{conf.WS}{conf.tso_utilities_streamer_endpoint}/subscribe"

        self.log_with_clock(log_level=logging.INFO,
                            msg=f"Establishing a connection to TSO data at {url}. ")
        try:
            async with websockets.connect(url) as websocket:
                self.log_with_clock(log_level=logging.INFO,
                                    msg=f"Connection to {url} for service data utilities is now active. ")
                while True:
                    try:
                        data = await websocket.recv()
                        message = json.loads(data)
                        if message['event'] in ['new_voting_round_initiated']:
                            self.log_with_clock(log_level=logging.INFO,
                                                msg=f"Got new schedule message for round {message['voting_round']}. ")

                            safe_ensure_future(self._schedule_queue.put(message))
                            self.log_with_clock(log_level=logging.INFO,
                                                msg=f"Waiting for the next TSO schedule message, "
                                                    f"from {self.schedule_source_keys}. ")
                            continue

                        self.utilities_message_processor(message=message)

                    except websockets.ConnectionClosed as cc:
                        self.log_with_clock(log_level=logging.ERROR,
                                            msg=f"Connection to {url} was closed. {cc}. Will re-establish connection. ")
                        await asyncio.sleep(1)
                        safe_ensure_future(self.tso_listener_loop(chain=chain))

                    except Exception as e:
                        self.log_with_clock(log_level=logging.ERROR,
                                            msg=f"Failed to connect to {url}. On message - {e}. ")
                        safe_ensure_future(self.tso_listener_loop(chain=chain))

        except Exception as e:
            self.log_with_clock(log_level=logging.ERROR,
                                msg=f"Failed to connect to {url}. On message - {e}. ")
            safe_ensure_future(self.tso_listener_loop(chain=chain))
