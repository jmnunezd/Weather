from credentials import key
import pandas as pd
pd.options.display.max_columns = 15
from urllib import request
import ast  # this library has a method to make str into dictionaries

# page_url: https://darksky.net/dev/docs

key = key()

weather = "https://api.darksky.net/forecast/" + key + "/10.29, -66.52"
resp = request.urlopen(weather).read().decode("UTF-8")

resp = ast.literal_eval(resp)  # dictionary
respdf = pd.DataFrame(resp["daily"]["data"])

print(respdf)
