from typing import Dict


class Trades:
    _shared_instance: "Trades" = None

    @classmethod
    def get_instance(cls) -> "Trades":
        if cls._shared_instance is None:
            cls._shared_instance = Trades()
        return cls._shared_instance

    def __init__(self):
        self.trades: Dict[int, list] = {}  # { stamp: list(trades) }
