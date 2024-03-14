# async_task_processor/utils.py
from datetime import datetime
from zoneinfo import ZoneInfo


class TimeHelper:
    timezone = "Europe/Amsterdam"

    def __init__(self, timezone: str = None) -> None:
        if timezone:
            self.timezone = timezone
        pass

    def get_current_time(self, timezone: str = None) -> datetime:
        if timezone:
            return datetime.now(ZoneInfo(timezone))
        return datetime.now(ZoneInfo(self.timezone))


time_helper = TimeHelper()
