import requests
from Const import RequestURL
from busClient import BusClient
import configparser
from datetime import datetime
from argparse import ArgumentParser

def wechat_notification(key, title, info):
    requests.get(
        url = RequestURL.wechatNotificationUrl % key,
        params={
            "title":title,
            "desp":info
        }
    )

if __name__ == '__main__':    
    parser = ArgumentParser()
    parser.add_argument('--USER', type=str)
    parser.add_argument('--PASSWORD', type=str)
    parser.add_argument('--KEY', type=str)
    argconf = parser.parse_args()

    config = configparser.ConfigParser()
    config.read("config.ini",encoding = "utf-8")

    client = BusClient()
    client.login(argconf.USER,argconf.PASSWORD)
    busList = client.retrieveBusInfo()
    now = datetime.now()

    success = busList != []

    for item in busList:
        if config["order"]["morning"] in item["action_stime"] or config["order"]["evening"] in item["action_stime"]:
            appoint_stime = datetime.strptime(item["appoint_stime"], "%Y-%m-%d %H:%M")
            if item["is_appoint"] == 0 and now >= appoint_stime:
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
        
    if config["notification"]["wechat"] == "True":
        print(sendTitle)
        print(info)
    else:
        print("no")
