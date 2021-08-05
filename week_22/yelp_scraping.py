#!/usr/bin/env python

from bs4 import BeautifulSoup as bs
from scrapy import Selector
import requests
import time
from flask import Flask, json, render_template, request, redirect
import os

app = Flask(__name__)

#decorator
@app.route("/")
def home_page():
    return "'<h1>Gather and Show Yelp Data</h1>\
    <p>/all for current yelp data.</p>\
    <p>/scrape to call scrape function and stores data. </p>"

@app.route("/all")
def all():
    json_url = os.path.join(app.static_folder,"","yelp_data.json")
    data_json = json.load(open(json_url))
    #render_template is always looking in templates folder, **templates plural
    return render_template('index.html',data=data_json)

@app.route("/scrape")
def scrape():
    yelp_restaurants = []
    top50 = [0,10,20,30,40]
    for i in top50:
        url = f'https://www.yelp.com/search?cflt=restaurants&find_loc=Ann%20Arbor%2C%20MI&start={i}'

        response = requests.get(url)
        soup = bs(response.text,'html.parser')

        for item in soup.select('[class*=container]'):
            try:
                
                if item.find('h4'):
                    name = item.find('h4').get_text() 
                    #print(name)
                    
                    rating = item.select('[aria-label *= rating]')[0]['aria-label']
                    #print(rating)
                    
                    foodType = item.find('p',class_="css-1j7sdmt").find('a').find('p',class_="text__09f24__2NHRu css-1hx6l2b").get_text()
                    #print(foodType)
                    
                    location = item.find('p',class_="css-1j7sdmt").find('span',class_="css-e81eai").get_text()
                    #print(location)
                    
                    if item.select('[class*=priceRange]'):
                        priceRange = item.select('[class*=priceRange]')[0].get_text()
                        #print(priceRange)
                    
                restaurant_dict = {"Restaurant Name":name,
                                   "Rating":rating,
                                   "Food Type":foodType,
                                   "Location":location,
                                   "Price Range":priceRange
                                  }
                yelp_restaurants = yelp_restaurants.append(restaurant_dict) 
            except Exception as e:
                printe(e)
    #return yelp_restaurants

    with open("./static/yelp_data.json",'r+') as file:
        file.seek(0)
        json.dump(yelp_restaurants,file,indent=4)

    #return render_template('index.html',data=yelp_restaurants)
    return redirect("/all")

if __name__ == "__main__":
    app.run(debug=True)