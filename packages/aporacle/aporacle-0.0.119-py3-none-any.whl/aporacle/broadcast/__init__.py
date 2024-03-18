import json
import logging
from typing import Optional

import websockets
from komoutils.core import KomoBase

from aporacle.conf import WS, streams


class DataBroadcaster(KomoBase):
    def __init__(self, stream: str = 'utilities'):
        self.url: str = f"{WS}{streams[stream]}/ingest"

    @property
    def name(self):
        return "data_broadcaster"

    async def send(self, data: list):
        try:
            assert type(data) == list, "Data must be a list of dictionaries."
            async with websockets.connect(self.url) as ws:
                for d in data:
                    await ws.send(json.dumps(d))
        except AssertionError as ae:
            self.log_with_clock(log_level=logging.ERROR, msg=f"Data format error. {ae}")
        except Exception as e:
            raise e

