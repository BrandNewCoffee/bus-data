import json
import requests
import time
access_token="eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJER2lKNFE5bFg4WldFajlNNEE2amFVNm9JOGJVQ3RYWGV6OFdZVzh3ZkhrIn0.eyJleHAiOjE3NzE3MTgzMDAsImlhdCI6MTc3MTYzMTkwMCwianRpIjoiYWI3OTMwMzEtOWFhZS00ZTUxLWEyYjYtNWU3YTljNGVkNmU3IiwiaXNzIjoiaHR0cHM6Ly90ZHgudHJhbnNwb3J0ZGF0YS50dy9hdXRoL3JlYWxtcy9URFhDb25uZWN0Iiwic3ViIjoiNDQzOTdjOWEtZGFkNC00MjNkLTk0YzAtNWI5ODllN2FkZDZkIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiMzEwNzU4LWYwYjJlMTA2LWEyNzUtNGU2NiIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsic3RhdGlzdGljIiwicHJlbWl1bSIsInBhcmtpbmdGZWUiLCJtYWFzIiwiYWR2YW5jZWQiLCJnZW9pbmZvIiwidmFsaWRhdG9yIiwidG91cmlzbSIsImhpc3RvcmljYWwiLCJjd2EiLCJiYXNpYyJdfSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwidXNlciI6ImY1ZWUzNjE5In0.pBgESUUg-6fCctTmTVTHShjRhKXxUm1nBha8zRuicz3y2m5mW4o12d04GJ1uY5kRiQ3IZjJxdnaXgHwCa3lDOpVwF7hQ0yAwlUTps7TR9CYLLE4VOsA5k6IKAs3JfGTsushtqyiiK-Kb-yZ9dbWlcQYt9xab2pOXSvvNAjOCDAN_7Gp8jp4TetwlAvykiZ8gvCDtrpPSm-Zo6t98javlSRzWC7TybT-UvsGa12lDp4L2szmxR3B1ZCCE6_YuCs6QBUIMv0A5b1BHQr9MSWalYbsBbK3QAWXHI_erD7sGotYTc75jYea72RRhCrLdauO_KDRl-6YMeql4rft9m1GHxQ"
headers = {
    "authorization": f"Bearer {access_token}"
}
routeList=["542"]#"234","南環幹線","205","618","民權幹線"]

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
    if not data:
        continue
    for subRoute in data:
        route_info = {
            "SubRoute": subRoute["SubRouteName"]["Zh_tw"],
            "Direction": subRoute["Direction"],
            "Stops": []
        }

        for stop in subRoute["Stops"]:
            route_info["Stops"].append({
                "Name": stop["StopName"]["Zh_tw"],
                "Lat": stop["StopPosition"]["PositionLat"],
                "Lon": stop["StopPosition"]["PositionLon"],
                "Sequence": stop["StopSequence"]
            })

        map_data.append(route_info)
    with open(f"data/stops/stops_{route}.json", "w", encoding="utf-8") as f:
        json.dump(map_data, f, ensure_ascii=False, indent=2)