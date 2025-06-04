from siliconflow import SiliconFlow
from amap import AmapAPI
import json


silicon_flow = SiliconFlow()


def test_siliconflow_generate_forecast():
    amap_api = AmapAPI()
    print(json.loads(silicon_flow.siliconflow_generate_forecast(amap_api.get_weather(extension="all"))))


def test_tell_jokes():
    print(silicon_flow.tell_jokes())
