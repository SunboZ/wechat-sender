# -*- coding: utf-8 -*-
# @Author: xhf
# @Date:   2024.4.1

import requests
import json
import datetime
import os
from utilities import get_rainbow

config_path = os.path.join(os.path.dirname(__file__), "config.json")


def llm_generate_forecast(amap_data):
    url = "https://ai-lab.feiliks.com/v1/completion-messages"

    payload = json.dumps({
    "inputs": {
        "query": f"content是高德地图返回的昆山市天气数据，根据数据播报明日天气，今天是{datetime.date}，语气要温柔可爱，发给女朋友的。返回的内容每行十五个字以内，总共六行，每一行严格按照我指定的内容描述。第一行只描述白天和夜间天气现象，是否下雨；第二行描述只白天和夜间气温；第三行只描述风向风力；第四行只描述穿衣建议和出行建议；第五行关心她；第六行夸赞女朋友的话，夸赞的话每天不重样。不要有其他客气官方的语言。<content>{amap_data}</content>"
    },
    "response_mode": "blocking",
    "user": "abc-123"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer app-MTcrZJjaEHh4oKB9NRKSE6jE'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    answer = response.json().get("answer")
    print(answer)
    return answer


def siliconflow_generate_forecast(amap_data):
    url = "https://api.siliconflow.cn/v1/chat/completions"

    payload = json.dumps({
    "model": "Qwen/Qwen3-235B-A22B",
    "messages": [
        {
            "role": "user",
            "content": f"content是高德地图返回的昆山市天气数据，根据数据播报明日天气，今天是{datetime.date}，语气要温柔可爱，发给女朋友的。返回的内容包括标点符号每行十三个字以内，总共六行，每一行严格按照后面我指定的内容描述。第一行描述白天和夜间天气现象，是否下雨；第二行描述气温区间，数字从小到大；第三行描述风向风力；第四行，提供穿衣建议；第五行关心她，每天不重样；第六行夸赞女朋友的话，每天不重样。每一行前面不要有序号，不要有多余的换行符，语气不要太客气和官方。<content>{amap_data}</content>"
        }
    ],
    "stream": False,
    "max_tokens": 512,
    "enable_thinking": False,
    "thinking_budget": 4096,
    "min_p": 0.05,
    "stop": None,
    "temperature": 0.7,
    "top_p": 0.7,
    "top_k": 50,
    "frequency_penalty": 0.5,
    "n": 1,
    "response_format": {
        "type": "text"
    },
    "tools": [
        {
            "type": "function",
            "function": {
                "description": "<string>",
                "name": "<string>",
                "parameters": {},
                "strict": False
            }
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer sk-yltpjsoivurxffuqigrxmzjjhggrmvqpdnqahyrpkhxhwzjz'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    answer = response.json().get("choices")[0].get("message").get("content")
    print(answer)
    return answer


# 从config.json中读取配置信息
def read_config():
    """
       读取配置文件并返回配置内容。

       Returns:
           dict: 包含配置信息的字典对象，如果文件不存在或解析失败，则返回空字典。
       """
    with open(config_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def updata_config():
    """
       将配置信息写入配置文件。

       Args:
           config_path (str): 配置文件路径。
       """
    with open(config_path, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4, ensure_ascii=False)

config = read_config()

# 从微信 API 获取访问令牌的函数
def get_stable_token(AppID=config["wechat"]["AppID"], AppSecret=config["wechat"]["AppSecret"]):
    """
            获取微信 access_token。

            Args:
                AppID (str): 微信应用的 AppID。
                AppSecret (str): 微信应用的 AppSecret。

            Returns:
                str: 获取到的 access_token。
            """
    url = "https://api.weixin.qq.com/cgi-bin/stable_token?"
    data = \
        {
            "grant_type": "client_credential",
            "appid": AppID,
            "secret": AppSecret
        }
    data = json.dumps(data)
    response = requests.post(url, data=data)

    res = response.json()
    print(res)
    # 更新配置文件
    access_token = res["access_token"]
    config["wechat"]["access_token"] = access_token

    updata_config()
    return access_token


def request_amap_forecat():
    """
        请求高德地图天气API获取天气数据。
        Args:
            location (str): 要获取天气数据的位置。
        Returns:
            dict: 包含天气数据的字典。
    """
    url2 = r'https://restapi.amap.com/v3/weather/weatherInfo?city=320583&extensions=all&output&Key=4f5a40a669b56882fe86809c26433e08'
    response2 = requests.get(url2)
    data2 = response2.json()
    print(data2)
    return data2
    

# 获取天气信息
def get_weather(location):
    """
        获取指定位置的天气信息。

        参数:
            location (str): 指定的位置信息。

        返回:
            dict: 包含天气信息的字典，包括以下键值对：
                - 'link' (str): 天气信息的链接。
                - 'date' (str): 日期。
                - 'city' (str): 城市名称。
                - 'temp' (dict): 包含温度信息的字典，包括 'today' 和 'now' 两个键值对，分别表示今天的最低和最高温度以及当前温度。
                - 'wea' (dict): 包含天气状况信息的字典，包括 'now'、'day'、'night' 和 'text' 四个键值对，分别表示当前天气、白天天气、夜晚天气以及总体天气描述。
                - 'win' (str): 风向和风力信息。
                - 'sun_time' (dict): 包含日出和日落时间的字典，分别表示 'sunrise' 和 'sunset'。

        异常:
            - requests.exceptions.RequestException: 网络请求异常。
            - json.JSONDecodeError: JSON解析异常。
        """
    city_id_url1 = r'https://restapi.amap.com/v3/geocode/geo?address={0}&key={1}'.format(location,
                                                                                         config['weather']['gd_key'])
    response_id = requests.get(city_id_url1)
    data_id = response_id.json()
    gd_cityid = data_id['geocodes'][0]['adcode']

    # 高德
    url1 = r'https://restapi.amap.com/v3/weather/weatherInfo?city={0}&key={1}'.format(
        gd_cityid, config['weather']['gd_key'])
    response1 = requests.get(url1)  # 发送请求获取天气信息
    data1 = response1.json()
    print(data1)


    url2 = r'https://restapi.amap.com/v3/weather/weatherInfo?city=320583&extensions=all&output&Key=4f5a40a669b56882fe86809c26433e08'
    response2 = requests.get(url2)
    data2 = response2.json()
    print(data2)

    # url3 = r'https://devapi.qweather.com/v7/weather/24h?location={0}&key={1}'.format(
    #     hf_cityid, config['weather']['hf_key'])
    # response3 = requests.get(url3)
    # data3 = response3.json()
    # print(data3)
    # 城市
    city = data1['lives'][0]['city']
    today_wheather = data2["forecasts"][0]["casts"][0]
    # 温度
    temp = {}
    temp['night'] = today_wheather['nighttemp'] + u'°C'
    temp['day'] = today_wheather['daytemp'] + u'°C'
    #
    # 天气状况
    weather = {}
    weather['now'] = today_wheather['dayweather']
    weather['day'] = today_wheather['dayweather']
    weather['night'] = today_wheather['nightweather']
    weather['text'] = None

    # 风向
    win = data1['lives'][0]['winddirection'] + u'风 ' + data1['lives'][0]['windpower'] + u'级'

    # 日期
    date = today_wheather["date"]

    sum_time = {}
    # 日出和日落时间
    sum_time["sunrise"] = None
    sum_time["sunset"] = None

    return {'link': "fxlink", 'date': date, 'city': city, 'temp': temp, 'wea': weather, 'win': win,
            "sun_time": "sum_time"}



# 纪念日
def get_love_day():
    """
        计算距离纪念日的天数。
        Returns:
            int: 距离纪念日的天数。
    """
    import datetime
    # 这里修改成自己的纪念日时间
    love_day = datetime.date(2025, 4, 15)
    now = datetime.datetime.now().date()
    delta = now - love_day
    return delta.days + 1


# 星期
def get_week():
    """
        获取当前星期。
        Returns:
            str: 当前星期的中文名称。
    """
    week = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    return week[datetime.datetime.now().weekday()]


def send_night_msg(touser, token, messages):
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={0}'.format(token)
    data = {
        "touser": touser,
        "template_id": "DWBib-AVOP9WImcprL8gom12cymtiaInWJ0Zi7V2rSo",
        "url": "https://www.qweather.com/",
        "topcolor": "#FF0000",
        "data": {
            "row1": {  # 星期
                "value": messages[0],
                "color": "#000"
            },
            "row2": {  # 星期
                "value": messages[1],
                "color": "#000"
            },
            "row3": {  # 星期
                "value": messages[2],
                "color": "#000"
            },
            "row4": {  # 星期
                "value": messages[3],
                "color": "#000"
            },
            "row5": {  # 星期
                "value": messages[4],
                "color": "#000"
            },
            "row6": {  # 星期
                "value": messages[5],
                "color": "#000"
            },
        }
    }
    response = requests.post(url=url, data=json.dumps(data))
    print(response.json())


# 发送消息
def send_message(touser, token, info, rainbow_text):
    """
        发送消息。
        Args:
            touser (str): 接收消息的用户 openid。
            token (str): 微信 access_token。
            info (dict): 包含天气信息的字典。
            rainbow_text (str): 彩虹屁文本。
    """
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={0}'.format(token)
    data = {
        "touser": touser,
        "template_id": config["template"]["template_id"],
        "url": "https://www.qweather.com/",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": info['date'],
                "color": "#000"
            },
            "city": {
                "value": info['city'],
                "color": "#000"
            },
            "weather_day": {
                "value": info['wea']['day'],
                "color": "#000"
            },
            "weather_night": {
                "value": info['wea']['night'],
                "color": "#000"
            },
            "temprature_day": {
                "value": info['temp']['day'],
                "color": "#000"
            },
            "temprature_night": {
                "value": info['temp']['night'],
                "color": "#000"
            },
            "rainbow": {
                "value": rainbow_text,
                "color": "#000"
            },
            "love_day": {
                "value": get_love_day(),
                "color": "#000"
            },
            "weektext": {  # 星期
                "value": get_week(),
                "color": "#000"
            },
        }
    }
    response = requests.post(url=url, data=json.dumps(data))
    if response.json()['errmsg'] == 'ok':
        print('\033[91m' + '推送成功' + '\033[0m')  # 输出红色文字
    else:
        print('\033[91m' + '推送失败' + '\033[0m')  # 输出红色文字


if __name__ == '__main__':
    #获取token,获取后会更新到配置文件中
    get_stable_token(config["wechat"]["AppID"], config["wechat"]["AppSecret"])

    # 从配置中获取token
    token =  config["wechat"]["access_token"]
    info = get_weather(location="昆山")  # 获取天气信息 # 把这里的location改为自己城市名字
    rainbow_text = get_rainbow()

    # 要推送的用户
    for user in config["template"]["touser"]:
        send_message(user, token, info, rainbow_text)
    # touser = config["template"]["touser"][1]
    # send_message(touser, token, info, rainbow_text)

    # 推送给多个用户：用for循环即可
    # 循环推送
    # for i in touser:
    #     send_message(i, token, info, rainbow_text)
