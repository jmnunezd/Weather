from credentials import key
import pandas as pd
pd.options.display.max_columns = 30
pd.set_option("display.width", 1000)
from urllib import request
import ast  # this library has a method to make str into dictionaries

# page_url: https://darksky.net/dev/docs

key = key()

weather1 = "https://api.darksky.net/forecast/" + key + "/10.29, -66.52"  # Caracas
weather2 = "https://api.darksky.net/forecast/" + key + "/4.35, -74.04"  # Bogota

resp1 = request.urlopen(weather1).read().decode("UTF-8")
resp2 = request.urlopen(weather2).read().decode("UTF-8")

resp1 = ast.literal_eval(resp1)  # dictionary
resp2 = ast.literal_eval(resp2)  # dictionary

respdf1 = pd.DataFrame(resp1["daily"]["data"])
respdf1["city"] = "Caracas"
respdf2 = pd.DataFrame(resp2["daily"]["data"])
respdf2["city"] = "Bogota"

print(respdf1)
print(respdf2)

