import json
import requests
import time
access_token="***"
headers = {
    "authorization": f"Bearer {access_token}"
}
routeList=[]

def get_data(url):
  response = requests.get(url, headers=headers)
  print(response.status_code,end=':')   # 通常是 200 表示成功
  if response.status_code!=200:
      print(response.text,end=':')
      return None
  return response.json()

for i in range(len(routeList)//5+1):
    for route in routeList[5*i:5*i+5]:
        map_data = []
        stops_url=f"https://tdx.transportdata.tw/api/basic/v2/Bus/StopOfRoute/City/Taipei/{route}?%24filter=RouteName%2FZh_tw%20eq%20%27{route}%27&%24top=30&%24format=JSON"
        data=get_data(stops_url)
        print(route)
        if not data:
            continue
        for subRoute in data:
            route_info = {
                "Route": subRoute["RouteName"]["Zh_tw"],
                "SubRoute": subRoute["SubRouteName"]["Zh_tw"],
                "Direction": subRoute["Direction"],
                "Stops": []
            }

            for stop in subRoute["Stops"]:
                route_info["Stops"].append({
                    "Name": stop["StopName"]["Zh_tw"],
                    "Lat": stop["StopPosition"]["PositionLat"],
                    "Lon": stop["StopPosition"]["PositionLon"],
                    "Sequence": stop["StopSequence"],
                    "StationID":stop["StationID"]
                })

            map_data.append(route_info)
        with open(f"../yesyes/data/stops/stops_{route}.json", mode="w", encoding="utf-8") as f:
            json.dump(map_data, f, ensure_ascii=False, indent=2)
    if 5*(i+1)>=len(routeList):
        break
    else:
        print(f"wait 60 seconds please. {len(routeList)-5*(i+1)} routes left.")
        time.sleep(60)