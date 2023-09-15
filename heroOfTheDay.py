### Import :
import hashlib
import time
import json
from pprint import pprint
import re
from random import randint

import tweepy
import requests

### Connection to the Marvel API :

m = hashlib.md5()

ts = str(time.time())
ts_byte = bytes(ts, 'utf-8')
m.update(ts_byte)
m.update(b"privateKey")

m.update(b"publicKey")
hasht = m.hexdigest() # hash = md5(ts+privateKey+publicKey)

print(hasht)

### Generation of the hero :

def heroOfTheDay():
    # Generate random id :
    id = randint(0, 1558)

    # Constructing the query :
    base_url = "https://gateway.marvel.com"
    api_key = ""
    query = "/v1/public/characters" + "?" + "offset=" + str(id) + "&"
    print(query_url)

    # Building the actual query from the information above
    query_url = base_url + query + "ts=" + ts + "&apikey=" + api_key + "&hash=" + hasht

    data = requests.get(query_url).json()

    # Making the API request and receiving info back as a json :
    data = requests.get(query_url).json()
    return data["data"]["results"][0]


### Text to tweet :
hero = heroOfTheDay()
name = hero["name"]
link = hero["urls"][0]["url"]
text = "🦸 Hero of the Day :\n Today our hero is ✨ " + name + " ✨\n \n" + "🔎 Find out more about our hero here : " + link + "\n \n #Marvel #HeroOfTheDay #" + \
       (name.replace(" ", "").replace(".", "").replace("-", "").replace(":", "")).split("(")[0]

### Image to tweet :
img = str(hero["thumbnail"]["path"]) + "/detail.jpg"
print(img)
open("./heroOfTheDay.jpg", "wb").write(requests.get(img).content)

while "image_not_available" in img:  # If image is not available, we pick an other hero
    # Text :
    hero = heroOfTheDay()
    name = hero["name"]
    link = hero["urls"][0]["url"]
    text = "🦸 What is our Hero today ?\n Today our hero is ✨ " + name + " ✨\n \n" + "🔎 Learn more about this hero here : " + link + "\n \n #Marvel #HeroOfTheDay #" + \
           (name.replace(" ", "").replace(".", "").replace("-", "").replace(":", "")).split("(")[0]
    # Image :
    img = str(hero["thumbnail"]["path"]) + "/detail.jpg"
    print(img)
    open("./heroOfTheDay.jpg", "wb").write(requests.get(img).content)

### Twitter connection :
consumer_key = "publicKey"
consumer_secret = "privateKey"
access_token = "publicAccessToken"
access_token_secret = "privateAccessToken"

client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(auth)

api.update_profile_image(filename="heroOfTheDay.jpg")
api.update_status_with_media(status=text, filename="heroOfTheDay.jpg")
