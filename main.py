import requests
from Const import RequestURL
from busClient import BusClient
import configparser
from datetime import datetime, timedelta, timezone
import os

def wechat_notification(key, title, info):
    responseBody = requests.get(
        url = RequestURL.wechatNotificationUrl % key,
        params={
            "text":title,
            "desp":info
        }
    )
    if responseBody.text == 'ok':
        print('微信提醒发送成功')
    else:
        print('微信提醒发送失败，返回信息：')
        print(responseBody.text)

if __name__ == '__main__':    

    config = configparser.ConfigParser()
    config.read("config.ini",encoding = "utf-8")

    user = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")    

    client = BusClient()
    client.login(user, password)
    busList = client.retrieveBusInfo()
    now = datetime.now(timezone(timedelta(hours=+8))).replace(tzinfo=None)
    print(now)

    success = busList != []

    for item in busList:
        if config["order"]["morning"] in item["action_stime"] or config["order"]["evening"] in item["action_stime"]:
            appoint_stime = datetime.strptime(item["appoint_stime"], "%Y-%m-%d %H:%M")
            if item["is_appoint"] != 0:
                print("校车" + item["action_stime"] + "已预约")
            elif now < appoint_stime:
                print("校车" + item["action_stime"] + "未开放，预约时间" + item["appoint_stime"])
            else:
                # 预约校车
                print("正在预约校车"+item["action_stime"]+"...")
                if not client.orderBus(int(item["id"])):
                    success = False

    busList = client.retrieveBusInfo()

    info = ""
    for item in busList:
        if item["is_appoint"] == 1:
            info += "预约" + item["action_stime"] + "成功\n"

    if success and busList != []:
        sendTitle = "预约成功"
    else:
        sendTitle = "预约失败"
        
    print('-'*60)
    print(sendTitle)
    print(info)
    print('-'*60)

    if config["notification"]["wechat"] == "True":
        sendkey = os.getenv('SENDKEY')
        print("正在发送微信提醒...")
        wechat_notification(sendkey, sendTitle, info)
