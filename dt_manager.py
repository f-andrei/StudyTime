from datetime import datetime, timedelta
from pytz import timezone
from typing import Optional, Tuple


class DateTimeManager:
    def __init__(self, tz: Optional[str] = None):
        self.tz = tz
        self.datetime_format = "%d/%m/%Y %H:%M:%S"
 
    def get_current_time(self) -> datetime:
        utc_now = datetime.utcnow()
        if self.tz:
            new_tz = timezone(self.tz)
            utc_now = utc_now.replace(tzinfo=timezone('UTC')).astimezone(new_tz)
        return utc_now

    def get_formatted_datetime_now(self) -> str:
        utc_now = self.get_current_time()
        if self.tz:
            new_tz = timezone(self.tz)
            formatted_tz_now = utc_now.replace(tzinfo=timezone('UTC')).astimezone(new_tz)
            formatted_tz_now = formatted_tz_now.strftime(self.datetime_format)
            return formatted_tz_now
        formatted_utc_now = utc_now.strftime(self.datetime_format)
        return formatted_utc_now

    def format_datetime(self, dt: datetime) -> str:
        formatted_datetime = dt.strftime(self.datetime_format)
        return formatted_datetime

    def get_due_tasks_time_range(self) -> Tuple[datetime, datetime]:
        current_time = self.get_current_time()
        end_time_range = current_time - timedelta(minutes=5)
        start_time_range = current_time + timedelta(seconds=10)

        return end_time_range, start_time_range

    def calculate_datetime(self, time: datetime, addendum: int) -> datetime:
        new_datetime = time + timedelta(minutes=addendum)
        return new_datetime