import json

import requests
from days import LoveDay, Today
from datetime import datetime
from utilities import get_rainbow


class WeChatOfficialAPI:
    def __init__(self):
        self.config = self.read_config()["wechat"]
        self.app_id = self.config["AppID"]
        self.app_secret = self.config["AppSecret"]

    @staticmethod
    def read_config():
        config_path =  "config.json"
        with open(config_path, 'r', encoding='utf-8') as file:
            return json.loads(file.read())
        
    @property
    def access_token(self):
        url = "https://api.weixin.qq.com/cgi-bin/stable_token?"
        data = \
            {
                "grant_type": "client_credential",
                "appid": self.app_id,
                "secret": self.app_secret
            }
        data = json.dumps(data)
        response = requests.post(url, data=data)

        res = response.json()
        # 更新配置文件
        access_token = res["access_token"]

        return access_token

    def send_template_message(self, touser, template_id, jump_url, data, top_color="#FF0000"):
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={0}'.format(self.access_token)
        data = {
            "touser": touser,
            "template_id": template_id,
            "url": jump_url,
            "topcolor": top_color,
            "data": data
        }
        response = requests.post(url=url, data=json.dumps(data))
        print(response.json())

    def send_night_msg(self, touser, messages, jump_url="https://www.qweather.com/"):
        data = {
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
            }
        }
        self.send_template_message(touser=touser, template_id="DWBib-AVOP9WImcprL8gom12cymtiaInWJ0Zi7V2rSo", jump_url=jump_url, data=data, top_color="#FFC0CB")

    def send_morning_msg(self, touser, info):
        data = {
                "date": {
                    "value": Today().chinese_description_date(),
                    "color": "#000"
                },
                "city": {
                    "value": "昆山",
                    "color": "#000"
                },
                "weather_day": {
                    "value": info['weather']['day'],
                    "color": "#000"
                },
                "weather_night": {
                    "value": info['weather']['night'],
                    "color": "#000"
                },
                "temprature_day": {
                    "value": info['temperature']['day'],
                    "color": "#000"
                },
                "temprature_night": {
                    "value": info['temperature']['night'],
                    "color": "#000"
                },
                "rainbow": {
                    "value": get_rainbow(),
                    "color": "#000"
                },
                "love_day": {
                    "value": LoveDay().days_count(),
                    "color": "#000"
                },
                "weektext": {  # 星期
                    "value": Today().weekday_cname(),
                    "color": "#000"
                },
            }
        self.send_template_message(touser=touser, template_id="DWBib-AVOP9WImcprL8gom12cymtiaInWJ0Zi7V2rSo", jump_url="https://www.qweather.com/", data=data, top_color="#FFC0CB")

