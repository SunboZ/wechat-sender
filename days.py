from datetime import datetime
from constants import WEEKDAYS


class Today:
    def __init__(self):
        self.date = datetime.today()

    def weekday_cname(self):
        return WEEKDAYS[self.date.weekday()]

    def chinese_description_date(self):
        return self.date.strftime("%Y年%m月%d日")


class Anniversary:
    def  __init__(self, date:datetime):
        self.date = date

    def days_left(self):
        today = datetime.today()
        anniversary_this_year = datetime(year=today.year, month=self.date.month, day=self.date.day)
        if anniversary_this_year < today:
            anniversary_next_year = datetime(year=today.year + 1, month=self.date.month, day=self.date.day)
            return (anniversary_next_year - today).days + 1
        else:
            return (anniversary_this_year - today).days + 1

    def days_count(self):
        today = datetime.today()
        return (today - self.date).days + 1


class LoveDay(Anniversary):
    def __init__(self):
        super().__init__(datetime(year=2025, month=4, day=15))

