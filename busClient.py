import requests
from Const import RequestURL
from numpy import random

class BusClient():

    __headers = {
                "Accept": "text/plain, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
            }

    def __init__(self, headers = __headers):
        self.__session = requests.session()

    def login(self, user, password, headers = __headers):
        for i in range(2):
            try:
                requestBody = self.__session.post(url=RequestURL.IaaaLoginUrl,
                                    headers=headers,
                                    data={
                                        "appid": "yywd",
                                        "userName": user,
                                        "password": password,
                                        "randCode":"",
                                        "smsCode":"",
                                        "otpCode":"",
                                        "redirUrl": RequestURL.IaaaRedirUrl
                                    }
                                    ).json()

                if requestBody["success"] != True:
                    print(requestBody["errors"]["msg"])
                    return
                
                # 单点登录
                self.__session.get(
                    url=RequestURL.IaaaSsoUrl,
                    headers=headers,
                    params={
                        "redirect":RequestURL.BusRetrieveApi,
                        "_rand":random.random(),
                        "token":requestBody["token"],
                    }
                )

                print("登录成功")
                return
            except Exception:
                print("登录异常，正在重试")

    def retrieveBusInfo(self, headers = __headers) -> list:
        # 返回当前订校车信息
        try:
            responseBody = self.__session.get(url=RequestURL.BusRetrieveApi,
                            headers=headers,
                            params={"id":40}
                            ).json()

            busList = responseBody["d"]["list"]
        except Exception:
            busList = []
            print("查询校车信息出现异常")
            print(Exception)

        return busList

    def orderBus(self, id, headers = __headers):
        try:
            req = self.__session.get(
                    url=RequestURL.BusCreateApi,
                        headers=headers,
                        data={
                            "id":id,
                            "roomid":""
                        }
                        )
                
            if "成功" in req.text:
                print("预约校车成功")
                return True
            else:
                print("预约校车失败")
                return False
        except Exception:
            print("预约校车出现异常")
            print(Exception)
            return False