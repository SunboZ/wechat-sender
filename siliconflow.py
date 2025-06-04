import datetime
import json
from urllib.parse import urljoin

import requests


class SiliconFlow:
    def __init__(self):
        self.auth_key = "sk-yltpjsoivurxffuqigrxmzjjhggrmvqpdnqahyrpkhxhwzjz"
        self.base_url = "https://api.siliconflow.cn"

    def chat(self, prompt, path="/v1/chat/completions"):
        url = urljoin(self.base_url, path)
        payload = json.dumps({
            "model": "Qwen/Qwen3-235B-A22B",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
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
            'Authorization': f'Bearer {self.auth_key}'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        answer = response.json().get("choices")[0].get("message").get("content")
        return answer

    def siliconflow_generate_forecast(self, amap_data):
        prompt = (f"content是高德地图返回的昆山市天气预报数据，"
                  f"根据数据播报明日天气，现在是{datetime.datetime.now()}，"
                  f"语气要温柔可爱，发给女朋友的。"
                  f"返回的内容包括标点符号每行十六个字以内，总共六行，"
                  f"每一行严格按照后面我指定的内容描述,"
                  f"第一行描述明天白天和夜间天气现象，是否下雨；"
                  f"第二行描述白天和夜间气温；"
                  f"第三行描述风向风力；"
                  f"第四行描述穿衣建议和出行建议；"
                  f"第五行关心她，每天不重样；"
                  f"第六行夸赞女朋友的话，每天不重样。"
                  f"每一行前面不要有序号，"
                  f"不要有多余的换行符，不要有其他客气官方的语言。"
                  f"返回的内容是json字符串，可以直接解析为字典，格式是 {{weather_emoji:str, rows: []}}"
                  f"<content>{amap_data}</content>")
        answer = self.chat(prompt)
        answer = answer.lstrip("```json").rstrip("```").strip()
        return answer

    def tell_jokes(self):
        return self.chat("讲一个笑话，直接说笑话，不要有其他的语句")