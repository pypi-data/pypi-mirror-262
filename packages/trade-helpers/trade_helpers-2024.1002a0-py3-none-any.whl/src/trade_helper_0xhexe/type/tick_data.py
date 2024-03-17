from datetime import datetime


class TickData:
    def __init__(self, high, low, close, _open, time, volume=0):
        if isinstance(time, int):
            time = datetime.fromtimestamp(time)

        self.high = high
        self.low = low
        self.close = close
        self.open = _open
        self.time = time
        self.volume = volume

    def __str__(self):
        return (
            f""
            f"Time: {self.time}, "
            f"Open: {self.open}, "
            f"High: {self.high}, "
            f"Low: {self.low}, "
            f"Close: {self.close}, "
            f"Volume: {self.volume}"
        )
