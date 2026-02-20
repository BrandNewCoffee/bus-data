import json
import requests
import time
access_token="eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJER2lKNFE5bFg4WldFajlNNEE2amFVNm9JOGJVQ3RYWGV6OFdZVzh3ZkhrIn0.eyJleHAiOjE3NzE2MjEzMTIsImlhdCI6MTc3MTUzNDkxMiwianRpIjoiZmYxNGMwNDctNWJhZC00OTU5LTgzMDAtNjlmNDQwYWY4MDM3IiwiaXNzIjoiaHR0cHM6Ly90ZHgudHJhbnNwb3J0ZGF0YS50dy9hdXRoL3JlYWxtcy9URFhDb25uZWN0Iiwic3ViIjoiNDQzOTdjOWEtZGFkNC00MjNkLTk0YzAtNWI5ODllN2FkZDZkIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiMzEwNzU4LWYwYjJlMTA2LWEyNzUtNGU2NiIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsic3RhdGlzdGljIiwicHJlbWl1bSIsInBhcmtpbmdGZWUiLCJtYWFzIiwiYWR2YW5jZWQiLCJnZW9pbmZvIiwidmFsaWRhdG9yIiwidG91cmlzbSIsImhpc3RvcmljYWwiLCJjd2EiLCJiYXNpYyJdfSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwidXNlciI6ImY1ZWUzNjE5In0.RhVfW8gNaYWAeGybJF7gkrhMZecDx6zLU34Sl78Ib8v6mpUaI24IIU0RP3V1CU-JUn8WkYtvnpxQ_maVp2Vxhf8IQ6UKRnrW8A3orSXAIqhwVnG5Om030wUbb3vnFtSBKzKvYpXKsJ60IZ-W_gWb0fCjIDpx7i3Xp7aKJblXjQQ0AdGK9zX7xtl3uE0hsw2kMTG-wN2BwzC7QEBrETL4UtGwwO7InfYs2SMtKUMfWmCoGROryua94xLACTvEroPGRQcaXDlwRfc9LwqLonAn-YGbIB_STLa-MONXBoHDTpyjNvLZ1G545RV6nzTOM69YAsUxyCB1m1UcYPEiB74R-w"
headers = {
    "authorization": f"Bearer {access_token}"
}
routeList=["234","南環幹線","205","618","民權幹線"]

def get_data(url):
  response = requests.get(url, headers=headers)
  print(response.status_code)   # 通常是 200 表示成功
  time.sleep(0.5)
  if response.status_code!=200:
      print(response.text)
      return None
  return response.json()

for route in routeList:
    map_data = []
    stops_url=f"https://tdx.transportdata.tw/api/basic/v2/Bus/StopOfRoute/City/Taipei/{route}?&%24format=JSON"
    data=get_data(stops_url)
    # if not data:
    #     continue
    for subRoute in data:
        route_info = {
            "route": subRoute["RouteName"]["Zh_tw"],
            "direction": subRoute["Direction"],
            "stops": []
        }

        for stop in subRoute["Stops"]:
            route_info["stops"].append({
                "name": stop["StopName"]["Zh_tw"],
                "lat": stop["StopPosition"]["PositionLat"],
                "lon": stop["StopPosition"]["PositionLon"],
                "sequence": stop["StopSequence"]
            })

        map_data.append(route_info)
    with open(f"data/stops/stops_{route}.json", "w", encoding="utf-8") as f:
        json.dump(map_data, f, ensure_ascii=False, indent=2)