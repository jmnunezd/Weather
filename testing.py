from credentials import key
import pandas as pd
from urllib import request
import ast

pd.options.display.max_columns = 30
pd.set_option("display.width", 1000)

key = key()

# --- Wrangling the data:
coordf = pd.read_csv("latitude&longitude.csv", sep=";")
coordf["lat_card"] = coordf["lat1"].apply(lambda row: row[-1])
coordf["lon_card"] = coordf["lon1"].apply(lambda row: row[-1])
coordf["lat"] = coordf["lat_card"].apply(lambda row: 1 if row == "N" else -1) * \
      (coordf["lat0"].astype("str") + "." + coordf["lat1"].apply(lambda row: row[:-2])).astype("float64")
coordf["lon"] = coordf["lon_card"].apply(lambda row: 1 if row == "E" else -1) * \
      (coordf["lon0"].astype("str") + "." + coordf["lon1"].apply(lambda row: row[:-2])).astype("float64")
coordf = coordf[["City", "lat", "lon"]]

# --- Creating a class that will handle everything:
class Coordinates(object):
    def __init__(self, latitude, longitude):
        self.lat = latitude
        self.lon = longitude

    def request_weather(self):
        weather = "https://api.darksky.net/forecast/" + key + "/%s,%s?units=ca" % (self.lat, self.lon)
        resp = request.urlopen(weather).read().decode("UTF-8")
        resp = ast.literal_eval(resp)
        respdf = pd.DataFrame(resp["daily"]["data"])
        return respdf

    def request_weather_list(self):
        cities = pd.DataFrame()
        for idx in coordf.index:
            slice = coordf.iloc[idx]
            lat = slice["lat"]
            lon = slice["lon"]
            city = Coordinates(lat, lon)
            city = city.request_weather()
            city["City"] = slice["City"]
            cities = cities.append(city)
        cities.reset_index(inplace=True)
        cities.rename(columns={"index": "days"}, inplace=True)
        cities.to_csv("global_weather_results.csv")
        return cities

# eg1:
san_francisco = Coordinates("37.72", "123.03")
print(san_francisco.request_weather())

#eg2:
all = Coordinates(0, 0)
print(all.request_weather_list())
