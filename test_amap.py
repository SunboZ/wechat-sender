from amap import AmapAPI


def test_get_weather():
    amap_api = AmapAPI()
    print(amap_api.get_weather(extension="all"))