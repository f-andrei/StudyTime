from datetime import datetime, timedelta
from pytz import timezone
from typing import Optional, Tuple


class DateTimeManager:
    def __init__(self, tz: Optional[str] = None):
        self.tz = tz
        self.datetime_format = "%Y-%m-%d %H:%M:%S"
        # self.datetime_format = "%d/%m/%Y %H:%M:%S"
 
    def get_current_time(self) -> datetime:
        datetime_now = datetime.utcnow()
        if self.tz:
            new_tz = timezone(self.tz)
            datetime_now = datetime_now.replace(tzinfo=timezone('UTC')).astimezone(new_tz)
        return datetime_now

    def get_day_number(self, datetime_str):
        dt_obj = datetime.strptime(datetime_str, "%Y-%m-%d")
        day_number = dt_obj.weekday()
        return (day_number + 1) % 7

    def get_formatted_datetime_now(self) -> str:
        datetime_now = self.get_current_time()
        formatted_datetime_now = datetime_now.strftime(self.datetime_format)
        return formatted_datetime_now

    def format_datetime(self, dt: datetime) -> str:
        formatted_datetime = dt.strftime(self.datetime_format)
        return formatted_datetime

    def get_due_tasks_time_range(self) -> Tuple[datetime, datetime]:
        current_time = self.get_current_time()
        end_time_range = current_time - timedelta(minutes=1, seconds=30)
        start_time_range = current_time + timedelta(seconds=10)

        end_time_range_str = end_time_range.strftime('%d/%m/%Y %H:%M:%S')
        start_time_range_str = start_time_range.strftime('%d/%m/%Y %H:%M:%S')

        _, end_time_range = end_time_range_str.split(' ')
        _, start_time_range = start_time_range_str.split(' ')

        return end_time_range, start_time_range

    def calculate_datetime(self, time: datetime, addendum: int) -> datetime:
        new_datetime = time + timedelta(minutes=addendum)
        return new_datetime






    