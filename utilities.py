import requests


# 彩虹屁
def get_rainbow():
    """
        获取彩虹屁。
        Returns:
            str: 彩虹屁文本。
    """
    url = 'https://v1.hitokoto.cn/'
    response = requests.get(url)
    data = response.json()
    print(data["hitokoto"])
    return data["hitokoto"]