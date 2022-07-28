import datetime

import requests
import sched
import time
from newsapi import NewsApiClient
import json
import os

from app.defintions import ROOT_DIR

news_articles = []
deleted_news = []

with open(os.path.join(ROOT_DIR,"config/", "config.json"), "r", encoding="utf-8") as config_file:
    # Open the configuration file and retrieve relevant settings
    CONFIG_NEWS = json.load(config_file)
    API_KEY = CONFIG_NEWS["News Section Configuration"]["APIkey"]


def news_API_request(covid_terms="Covid COVID-19 coronavirus"):
    """Finds all results pertaining to Covid-19 ("Covid" "Covid 19" or coronavirus" ) from News API. "Covid" "Covid
    19" or coronavirus" arguments are passed by default. Note: News API no longer works in the United Kingdom and can
    therefore only be used through a VPN to function properly. Returns API response in Json format. """

    words = covid_terms.split(" ")
    search_query = ' OR '.join(words)

    previous_date = datetime.datetime.today() - datetime.timedelta(days=2)
    news_date_set = str(previous_date)

    url = ('https://newsapi.org/v2/everything?'
           f'qInTitle={search_query}&'
           f'from={news_date_set}&'
           'sortBy=popularity&'
           'language=en&'
           f'apiKey={API_KEY}')

    response = requests.get(url).json()



    # newsapi = NewsApiClient(api_key='8eb0811e2ad440c6b3cbda083ccd7f46')
    # data_handler = newsapi.get_everything(q=search_query, language='en', page_size=20)
    # return data_handler

    return response


def global_news_API_request():
    """Stores data returned by news_API_request() in global variable, which can in turn be used in
        updates_news1 function """
    global info
    info = news_API_request()


def update_news():
    """Uses the news_API_request function to update a data structure containing news articles. Checks that
    articles deleted by user are not included in the update. Returns dictionary of articles."""
    data = news_API_request()
    news_articles = data['articles']
    # Need to check for any deleted items and prevent them from being reloaded
    for article in news_articles:
        if article in deleted_news:
            news_articles.remove(article)
    return news_articles



def update_news1(update_interval, update_name):
    """Returns news data structure after specified period of time. Arguments include update interval in seconds and
        update name respectively"""
    timer = sched.scheduler(time.time, time.sleep)
    timer.enter(float(update_interval), 1, global_news_API_request, )
    timer.run()
    news_articles = info
    return news_articles
