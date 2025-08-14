import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


API_KEY = os.getenv("API_KEY")
url = (
    "https://api.eia.gov/v2/electricity/rto/region-sub-ba-data/data/"
    "?api_key={}&frequency=hourly&facets[parent][]=CISO&facets[subba][]=PGAE"
    "&data[]=value&start=2024-06-01T00&end=2024-06-07T23&offset=0&length=5000"
).format(API_KEY)

response = requests.get(url)
data = response.json()["response"]["data"]

df = pd.DataFrame(data)
# Rename columns to match your schema
df = df.rename(columns={
    "subba": "region",
    "value": "demand",
    "period": "timestamp"
})
# If supply data is not present, you may need to query a different endpoint or supplement it.
df["supply"] = None  # or populate with actual supply data if available

df.to_csv("./gridstate.csv", index=False)
