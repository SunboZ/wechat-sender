from amap import AmapAPI


def test_get_weather():
    amap_api = AmapAPI()
    amap_api.get_weather()
