import time
import json
import requests

DESC = "C:\\Users\\CuiRH\\GitHub\\Covid-19-Map\\public\\static\\info.json"

overallRsp = requests.get("https://lab.isaaclin.cn/nCoV/api/overall?latest=1")
overall = overallRsp.json()["results"][0]

time.sleep(3)

detailRsp = requests.get("https://lab.isaaclin.cn/nCoV/api/area?latest=1", timeout=20)
detail = detailRsp.json()["results"]

maps = {
    "United States of America": "United States",
    "Russian Federation": "Russia",
    "Republic of Korea": "Korea",
    "Bolivia (Plurinational State of)": "Bolivia",
    "Democratic Republic of the Congo": "Dem. Rep. Congo",
    "The Republic of Zambia": "Zambia",
    "Central African Republic": "Central African Rep.",
    "The Republic of Burundi": "Burundi",
    "The Republic of Haiti": "Haiti",
    "Dominican Republic": "Dominican Rep.",
    "The United Kingdom": "United Kingdom",
    "Cote d Ivoire": "Côte d'Ivoire",
    "South Sudan": "S. Sudan",
    "The Republic of Yemen": "Yemen",
    "The Republic of Djibouti": "Djibouti",
    "Iran (Islamic Republic of)": "Iran",
    "Uzbekstan": "Uzbekistan",
    "Laos": "Lao PDR",
    "Syrian ArabRepublic": "Syria",
    "Czechia": "Czech Rep.",
    "Bosnia and Herzegovina": "Bosnia and Herz.",
    "North Macedonia": "Macedonia",
    "Republic of Moldova": "Moldova"
}

chinaData = []
worldData = []
for item in detail:
    if item["countryName"] == "中国" and item["provinceName"] != "中国":
        chinaData.append(
            {
                "name": item["provinceShortName"],
                "provinceName": item["provinceShortName"],
                "value": item["currentConfirmedCount"],
            }
        )
    else:
        if(item["countryFullName"] in maps):
            item["countryFullName"] = maps[item["countryFullName"]]
        worldData.append(
            {
                "name": item["countryFullName"],
                "provinceName": item["countryName"],
                "value": item["currentConfirmedCount"],
            }
        )

data = {
    "china": {
        "currentConfirmedCount": overall["currentConfirmedCount"],
        "confirmedCount": overall["confirmedCount"],
        "deadCount": overall["deadCount"],
        "curedCount": overall["curedCount"],
    },
    "world": {
        "currentConfirmedCount": overall["globalStatistics"]["currentConfirmedCount"],
        "confirmedCount": overall["globalStatistics"]["confirmedCount"],
        "deadCount": overall["globalStatistics"]["deadCount"],
        "curedCount": overall["globalStatistics"]["curedCount"],
    },
    "chinaDetail": chinaData,
    "worldDetail": worldData,
}
# print(data)
with open(DESC, "w") as f:
    json.dump(data, f)
