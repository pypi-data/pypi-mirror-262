from typing import Optional


class SharedData:
    _shared_instance: "SharedData" = None

    @classmethod
    def get_instance(cls) -> "SharedData":
        if cls._shared_instance is None:
            cls._shared_instance = SharedData()
        return cls._shared_instance

    def __init__(self):
        self.current_chain_epoch: dict = {}
        self.current_tso_prices: dict = {"coston": float, "songbird": float, "flare": float}

        self.last_close: Optional[float] = None
        self.last_returns: dict = {"coston": 0.0, "flare": 0.0, "songbird": 0.0}

