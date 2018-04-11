from wxpy import *
import requests
import json
bot = Bot()
# 然后扫描二维码登陆
# 查找名为xxx的微信好友
friend = bot.friends().search("")[0]
def auto_reply(text):
    """调用 tuling 聊天机器人API，将text发送给图灵机器人，返回收到的消息"""
    url = "http://www.tuling123.com/openapi/api"
    api_key = ""
    payload = {
            "key": api_key,
            "info":text,
            "userid":"123456"
            }
    r = requests.post(url,data=json.dumps(payload))
    result = json.loads(r.content)
    return result["text"]

# 注册
@bot.register(friend)
def forward(msg):
    return auto_reply(msg.text)
