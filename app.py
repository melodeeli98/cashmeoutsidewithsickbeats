#--coding: utf-8 --
from flask import Flask, make_response, jsonify, render_template, request
from geolocation.main import GoogleMaps
from geolocation.distance_matrix.client import DistanceMatrixApiClient
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from pprint import pprint

app = Flask(__name__,static_url_path="/static",static_folder="static")

@app.route('/weather',methods=['POST'])
def hello_world():
    #client_credentials_manager = SpotifyClientCredentials()
    #sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    #return make_response(jsonify(sp.user_playlists('spotify')),200)
    zipcode= request.form['text']
    link1="http://api.openweathermap.org/data/2.5/weather?zip="
    link2=",us&APPID=4a4fd9ff55bc2bc303555b016dcc849b"
    fullLink=link1+zipcode+link2
    r = requests.get(fullLink)

    data=json.loads(r.text)
    weather=(data["weather"][0]["description"])
    if weather=="few clouds"or weather=="scattered clouds" or weather=="broken clouds":
        weather="partly cloudy"
    elif weather=="rain" or weather=="shower rain" or weather=="light rain":
        weather="rainy"

    urlDict=dict()
    urlDict["partly cloudy"]="spotify:user:melonmelly:playlist:1tMhJmOeyNjnHO5neqYU4I"
    urlDict["clear sky"] = "spotify:user:melonmelly:playlist:1HXaJIWatWQejgjrKycyrA"
    urlDict["rainy"] = "spotify:user:melonmelly:playlist:3Wc03PVxVtmdAFQkcn4Eed"
    urlDict["thunderstorm"] = "spotify:user:melonmelly:playlist:7vNVtd2AX7MpdZxKBuz8VI"
    urlDict["snow"] = "spotify:user:melonmelly:playlist:5FEB90fqEZPf9K9tJQGba0"
    urlDict["mist"] = "spotify:user:melonmelly:playlist:1HXaJIWatWQejgjrKycyrA"

    try:
        url=urlDict[weather]
    except: raise Exception(':('+weather+"doesn't exist in the dictionary")

    return render_template("weather.html",weather=weather.title(),url=url,zipcode=zipcode)

@app.route('/')
def get_zipcode():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)
