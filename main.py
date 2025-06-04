import json

from amap import AmapAPI
from siliconflow import SiliconFlow
from wechat_official import WeChatOfficialAPI


def send_morning_msg():
    silicon_flow = SiliconFlow()
    amap_api = AmapAPI()
    data = json.loads(silicon_flow.siliconflow_generate_forecast(amap_api.get_weather(extension="all")))
    messages = data.get("rows")
    wechat_api = WeChatOfficialAPI()
    wechat_api.send_night_msg(touser="o63nA7epqUGoyUy1MWjSBix7tLYA", messages=messages)


def send_morning_msg():
    pass