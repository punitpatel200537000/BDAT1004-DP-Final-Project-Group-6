from flask import Flask, render_template
from pymongo import MongoClient
import requests
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# connect to MongoDB database
client = MongoClient("mongodb+srv://weather-app:weather@weather.zpkctj5.mongodb.net/?retryWrites=true&w=majority")
db = client["Weather"]
collection = db["forecast"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/temp/chart")
def temp():
    # retrieve the first document in the collection
    document = collection.find_one()
    # retrieve the value of the "datetime" key
    data = document["data"]
    # render the value in an HTML template
    return render_template("temp-chart.html", data=data)

@app.route("/wind/chart")
def wind():
    # retrieve the first document in the collection
    document = collection.find_one()
    # retrieve the value of the "datetime" key
    data = document["data"]
    # render the value in an HTML template
    return render_template("wind-chart.html", data=data)

@app.route("/ozone/chart")
def ozone():
    # retrieve the first document in the collection
    document = collection.find_one()
    # retrieve the value of the "datetime" key
    data = document["data"]
    # render the value in an HTML template
    return render_template("ozone-chart.html", data=data)

# create a scheduler object
scheduler = BackgroundScheduler()

# define the task to be scheduled
def collection_update():
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
    for entry in data:
        collection.insert_one(entry)

# add the task to the scheduler
scheduler.add_job(collection_update, 'interval', hours=24)

# start the scheduler
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)