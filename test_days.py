import datetime

from days import LoveDay, Today
from days import Anniversary


def test_love_day():
    day = LoveDay()
    print(day.date)


def test_anniversary():
    day = LoveDay()
    print(day.days_count())


def test_today():
    day = Today()
    print(day.chinese_description())
