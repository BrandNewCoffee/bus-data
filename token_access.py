import requests
import json
from pprint import pprint

app_id = '310758-f0b2e106-a275-4e66'
app_key = '1862cdc6-8f5d-47c3-8aa2-b78f2b943815'

auth_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
url = "https://tdx.transportdata.tw/api/basic/v2/Bus/Route/City/Taipei/612?%24top=10&%24format=JSON"

# 取得 token
def get_token():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": app_id,
        "client_secret": app_key
    }
    resp = requests.post(auth_url, headers=headers, data=data)
    resp_json = resp.json()

    if "access_token" not in resp_json:
        print("取得 Token 失敗：")
        print(resp_json)
        return None
    
    return resp_json["access_token"]

# 使用 token 呼叫 API
def call_api(token):
    headers = {
        "Authorization": "Bearer " + token,
        "Accept-Encoding": "gzip"
    }
    resp = requests.get(url, headers=headers)
    return resp.json()

if __name__ == "__main__":
    token = get_token()

    if token is None:
        print("無法取得 Token，請檢查 app_id/app_key")
    else:
        data = call_api(token)
#        pprint(data)
        print(token)
