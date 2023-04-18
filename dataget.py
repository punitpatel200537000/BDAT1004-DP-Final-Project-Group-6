import requests
from pymongo import MongoClient

# connect to MongoDB database
client = MongoClient("mongodb+srv://weather-app:weather@weather.zpkctj5.mongodb.net/?retryWrites=true&w=majority")
db = client["Weather"]
collection = db["forecast"]

# clear existing data from collection
collection.delete_many({})

api_key = "615b7b7d8be249f5a9108a6c14d41b1e"

# fetch data from REST Countries API
url = f"https://api.weatherbit.io/v2.0/forecast/daily?&city=Barrie&country=CA&key={api_key}"
response = requests.get(url)
data = response.json()

# insert data into MongoDB collection
collection.insert_one(data)


