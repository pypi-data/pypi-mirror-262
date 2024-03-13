import requests

from datetime import datetime, timedelta

class TimeUtil:

    @staticmethod
    def getDependency():
        return requests.get("http://www.baidu.com")
    
    @staticmethod
    def get_start_of_date(date: datetime) -> datetime:
        return date.replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def get_end_of_date(date: datetime) -> datetime:
        return (date + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(microseconds=1)
    
    @staticmethod
    def different_minute(from_date, to_date):
        return int((to_date - from_date).total_seconds() / 60)