from urllib.parse import urljoin
import requests


class AmapAPI:
    key = "4f5a40a669b56882fe86809c26433e08"

    def __init__(self):
        self.base_url = "https://restapi.amap.com"

    def get_weather(self, city="320583", extension="base", path="/v3/weather/weatherInfo"):
        """

        :param city:
        :param extension: base返回实时天气，all返回预报天气
        :param path:
        :return:
        """
        url = urljoin(self.base_url, path)
        query_params = {
            "city": city,
            "extension": extension,
            "Key": self.key
        }
        res = requests.get(url, params=query_params)
        return res.json()