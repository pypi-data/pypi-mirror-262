# Topics - Get from db
import asyncio
import json
import logging
from typing import Dict, List

import pendulum
from komoutils.core import KomoBase, SubscribeRequest, safe_ensure_future, PublishQueue
from komoutils.core.time import the_time_in_iso_now_is
from starlette.websockets import WebSocket, WebSocketDisconnect


class SubscriptionsConnectionManager(KomoBase):
    def __init__(self, broadcast_queue: asyncio.Queue, topics: list, tag: str):
        self.broadcast_queue: asyncio.Queue = broadcast_queue
        self.topics: list = topics
        self.tag: str = tag
        self.subscriptions: Dict[str, List[WebSocket]] = {}
        self.broadcast_loop_task = safe_ensure_future(self.broadcast_loop())

    async def subscribe(self, websocket: WebSocket, request: SubscribeRequest):
        subscribed: list = []

        for topic in request.topics:
            if topic not in self.topics:
                self.log_with_clock(log_level=logging.WARNING, msg=f"{topic} is not a valid topic. ")
                continue

            if topic not in self.subscriptions:
                self.subscriptions[topic] = []

            self.subscriptions[topic].append(websocket)
            subscribed.append(topic)

        # Only accept the connection if there is a topic to be served on that connection.
        if len(subscribed) > 0:
            message = {"success": f"Successfully connected to {len(subscribed)} topics. "}
            await websocket.send_text(json.dumps(message))
            self.log_with_clock(log_level=logging.INFO, msg=f"A connection has successful subscribed to "
                                                            f"{len(subscribed)} topics. {subscribed}. ")
        else:
            await websocket.close(code=429, reason="Provided topic(s) invalid. ")
            self.log_with_clock(log_level=logging.WARNING, msg=f"A connection attempt was not completed because no "
                                                               f"valid topics were submitted. ")

    async def unsubscribe(self, websocket: WebSocket):
        for topic in self.subscriptions:
            if websocket in self.subscriptions[topic]:
                self.log_with_clock(log_level=logging.INFO, msg=f"Unsubscribing a client from {topic}. ")
                self.subscriptions[topic].remove(websocket)

    async def broadcast(self, message: dict):
        topic: str = message['topic']
        if topic not in self.subscriptions:
            return

        # print(message)
        for connection in self.subscriptions[topic]:
            message[f'time_dispatched_from_{self.tag}'] = the_time_in_iso_now_is()
            try:
                await connection.send_text(json.dumps(message))
            except WebSocketDisconnect as wde:
                self.log_with_clock(log_level=logging.WARNING, msg=f"A client has disconnected. {wde}")
                await self.unsubscribe(websocket=connection)
            except Exception as e:
                print(e.__class__.__name__)
                # raise e

    async def broadcast_loop(self):
        self.log_with_clock(log_level=logging.INFO, msg=f"Starting broadcast loop for {len(self.topics)}. ")
        while True:
            message = await self.broadcast_queue.get()
            safe_ensure_future(self.broadcast(message=message))


class IngestorConnectionManager(KomoBase):
    def __init__(self, output: PublishQueue, tag: str):
        self.output = output
        self.tag = tag
        self.connections: list[WebSocket] = []

        # safe_ensure_future(self.fake_data_loop())

    @property
    def name(self):
        return f"ingestor_connection_manager"

    async def connect(self, websocket: WebSocket):
        """connect event"""
        await websocket.accept()
        self.connections.append(websocket)
        self.log_with_clock(log_level=logging.INFO, msg=f"A client just connected to {self.name}. ")

    async def message_received(self, message: dict, websocket: WebSocket):
        """Direct Message"""
        message[f'time_of_arrival_at_{self.tag}'] = the_time_in_iso_now_is()
        self.output.publish(message)

    def disconnect(self, websocket: WebSocket):
        """disconnect event"""
        self.connections.remove(websocket)
        self.log_with_clock(log_level=logging.INFO, msg=f"A client just disconnected from {self.name}. ")

    # async def fake_data_loop(self):
    #     while True:
    #         await asyncio.sleep(1)
    #         data = {'test': 'test',
    #                 'type': 'trades',
    #                 'symbol': 'BINANCE_SPOT_BTC_USDT',
    #                 'time': pendulum.now('UTC').to_iso8601_string()}
    #         print(data)
    #         self.output.publish(data)
