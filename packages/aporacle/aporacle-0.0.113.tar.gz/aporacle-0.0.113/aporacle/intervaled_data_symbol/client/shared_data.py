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
        self.current_tso_prices: dict = {"songbird": float, "flare": float}

        self.last_close: Optional[float] = None
        self.last_returns: dict = {"flare": 0.0, "songbird": 0.0}

    # def set(self, epoch_data: dict):
    #     end_time = epoch_data["end_time"] - SharedSetup.get_instance().end_time_execution_buffer - 1
    #     start_time = epoch_data["start_time"] - SharedSetup.get_instance().end_time_execution_buffer
    #
    #     self.current_chain_epoch[epoch_data["chain"]] = {
    #         "epoch": epoch_data["epoch_id"],
    #         "start": start_time,
    #         "end": end_time,
    #         "st_str": epoch_data["st_str"],
    #         "et_str": epoch_data["et_str"],
    #     }
