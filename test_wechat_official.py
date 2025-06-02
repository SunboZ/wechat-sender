from wechat_official import WeChatOfficialAPI


def test_send_template_message():
    wechat_api = WeChatOfficialAPI()
    wechat_api.send_night_msg(touser="o63nA7epqUGoyUy1MWjSBix7tLYA", messages=[i for i in range(6)])
