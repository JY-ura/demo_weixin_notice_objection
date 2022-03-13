import json
import requests

# 1. 获取access_token
#https请求方式: GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET

app_ID = 'wx8c6505f83a2b9810'
app_secret = '24b248d7c712ee034128b1fba70c9c24'
url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_ID}&secret={app_secret}'
#print(url)
resp = requests.get(url).json()
#print(resp)
access_token = resp.get('access_token')


# 2. 利用access_token发送微信通知
# http请求方式: POST https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=ACCESS_TOKEN

url=f'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={access_token}'
#print(url)
open_id = 'oJz3l6FM6wdMvFi9FNBZGYEfl3bw'
req_data = {
    "touser": open_id,
    "msgtype":"text",
    "text":
    {
         "content":"有人闯入！"
    }
}
req_str= json.dumps(req_data , ensure_ascii = False)
req_data = req_str.encode('utf-8')
requests.post(url, data = req_data)