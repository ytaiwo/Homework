#!/usr/bin/env python

from bs4 import BeautifulSoup as bs
from scrapy import Selector
import requests
import pandas as pd
from flask import Flask, json, render_template, request
import os

#decorator
@app.route("/")
def home_page():
    return "'<h1>Gather and Show Yelp Data</h1>\
    <p>/all for current yelp data.</p>\
    <p>/scrape to call scrape function and stores data. </p>"
    
@app.route("/scrape")
def scrape():
    top50 = [0,10,20,30,40]
    for i in top50:
        url = f'https://www.yelp.com/search?cflt=restaurants&find_loc=Ann%20Arbor%2C%20MI&start={i}'

        response = requests.get(url)
        soup = bs(response.text,'html.parser')

        for item in soup.select('[class*=container]'):
            try:
                
                if item.find('h4'):
                    name = item.find('h4').get_text() 
                    print(name)
                    
                    rating = item.select('[aria-label *= rating]')[0]['aria-label']
                    print(rating)
                    
                    foodType = item.find('p',class_="css-1j7sdmt").find('a').find('p',class_="text__09f24__2NHRu css-1hx6l2b").get_text()
                    print(foodType)
                    
                    location = item.find('p',class_="css-1j7sdmt").find('span',class_="css-e81eai").get_text()
                    print(location)
                    
                    if item.select('[class*=priceRange]'):
                        priceRange = item.select('[class*=priceRange]')[0].get_text()
                        print(priceRange)
                    
                    print('\n') 
            except Exception as e:
                raise e 
                print('')

if __name__ == "__main__":
    app.run(debug=True)