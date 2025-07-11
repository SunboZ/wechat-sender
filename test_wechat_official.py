import json

from amap import AmapAPI
from siliconflow import SiliconFlow
from wechat_official import WeChatOfficialAPI


def test_send_template_message():
    silicon_flow = SiliconFlow()
    amap_api = AmapAPI()
    data = json.loads(silicon_flow.siliconflow_generate_forecast(amap_api.get_weather(extension="all")))
    emoji = data.get("weather_emoji")
    messages = data.get("rows")
    messages[0] = messages[0][0:2] + emoji + messages[0][2:]
    wechat_api = WeChatOfficialAPI()
    print(messages)
    wechat_api.send_night_msg(touser="o63nA7epqUGoyUy1MWjSBix7tLYA", messages=messages)
