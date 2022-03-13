import json
import requests

class WxTools():
    def __init__(self,app_id,app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    def get_access_token(self):
        url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}'
        resp = requests.get(url).json()
        access_token = resp.get('access_token')
        return access_token

    def send_wx_customer_msg(self, open_id, msg="有人闯入"):
        url = f'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={self.get_access_token()}'
        # print(url)
        open_id = 'oJz3l6FM6wdMvFi9FNBZGYEfl3bw'
        req_data = {
            "touser": open_id,
            "msgtype": "text",
            "text":
                {
                    "content": msg
                }
        }
        req_str = json.dumps(req_data, ensure_ascii=False)
        req_data = req_str.encode('utf-8')
        requests.post(url, data=req_data)


if __name__ == "__main__":
    app_ID = 'wx8c6505f83a2b9810'
    app_secret = '24b248d7c712ee034128b1fba70c9c24'
    wx_tools = WxTools('wx8c6505f83a2b9810', '24b248d7c712ee034128b1fba70c9c24')
    wx_tools.send_wx_customer_msg('oJz3l6FM6wdMvFi9FNBZGYEfl3bw')



