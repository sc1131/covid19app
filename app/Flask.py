import json
import logging
import os
from flask import Flask, render_template, request
from app.data_handler.covid_data_handler import covid_API_request
from datetime import datetime, date, timedelta
from app.news_handler.covid_news_handling import update_news
from apscheduler.schedulers.background import BackgroundScheduler


class CovidApp:
    """This is a class called Covid App which manages all the essential functions of the dashboard"""
    def __init__(self):
        with open("app/config/config.json", "r", encoding="utf-8") as config_file:
            config_data = json.load(config_file)
            self.image = config_data['Image']['imagePath']
        logging.basicConfig(level=logging.DEBUG,
                            filename=os.path.join("app/logs/", "app.log"),
                            filemode="a",
                            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                            datefmt="%d-%b-%y %H:%M:%S")
        self.updates = []
        self.news_articles = []
        self.deleted_articles = []
        self.local_7day_infections = 0
        self.national_7day_infections = 0
        self.location = config_data['Covid Data Configuration']["Location"]

        self.nation_location = config_data['Covid Data Configuration']["Nation"]
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def process_update(self, label_box, repeat_box, covid_data_box, news_box, datetime_object):
        """Updates dashboard in accordance with which checkboxes have been ticked: includes news, Covid-19 info,
        repeat, scheduled updates by time. Used when scheduling updates"""
        if covid_data_box is not None:
            self.local_covid_data_update()
            self.national_covid_data_update()

        if news_box is not None:
            self.news_update()

        for update in self.updates:
            if update['title'] == label_box:
                self.updates.remove(update)
                logging.debug("Update window removed")

        if repeat_box is not None:
            tomorrow = datetime_object + timedelta(days=1)
            self.updates.append({'title': 'Repeat: ' + label_box, 'content': tomorrow})
            logging.debug("Add reminder window same time in 24 hours time if 'repeat' selected")
            self.scheduler.add_job(func=self.process_update, args=(label_box, repeat_box, covid_data_box, news_box),
                                   trigger="date",
                                   run_date=tomorrow)
            logging.debug("Schedule reminder for specified time")

    def __covid_data_update(self, mode):
        """'Updates Covid info, locally or nationally based on mode parameter. Provides data for number of infections
        in last seven days. Stores data in fields: 'local_7day_infections' or 'national_7day_infections' """
        covid_info = None
        try:
            if mode == 'Local':
                covid_info = covid_API_request()
            elif mode == 'National':
                covid_info = covid_API_request('England', 'nation')
            logging.debug(f"{mode} Covid data updated")
        except:
            logging.critical("Unable to reach COVID api")
            return None

        infections = 0
        for day in range(7):
            infections += covid_info['data'][day]['newCasesByPublishDate']
        logging.debug(f"{mode} 7 day infections updated")

        if mode == 'Local':
            self.local_7day_infections = infections

        elif mode == 'National':
            self.national_7day_infections = infections

    def local_covid_data_update(self):
        """Updates local Covid info and stores it in 'local_7day_infections' """
        self.__covid_data_update('Local')

    def national_covid_data_update(self):
        """Updates local Covid info and stores it in 'national_7day_infections' """
        self.__covid_data_update('National')

    def news_update(self):
        """Updates news and stores in "news_articles" field. """
        try:
            self.news_articles = update_news()
            logging.debug("News articles updated")
        except:
            logging.critical("Unable to reach News API")

    def start_app(self):
        """Run server and load dashboard. """
        app = Flask(__name__)
        app.config['SERVER_NAME'] = '127.0.0.1:5000'

        @app.route('/')
        def page():

            self.local_covid_data_update()
            self.national_covid_data_update()
            self.news_update()

            return render_template('index.html',
                                   image=self.image,
                                   updates=self.updates,
                                   news_articles=self.news_articles,
                                   location=self.location,
                                   local_7day_infections=self.local_7day_infections,
                                   nation_location=self.nation_location,
                                   national_7day_infections=self.national_7day_infections)

        @app.route('/update', methods=['POST', 'GET'])
        def update():
            """Returns dashboard with updated information specified by the user on local server."""

            data = request.get_json()
            self.updates = data['updates']
            self.news_articles = data['news_articles']
            self.national_7day_infections = data['national_7day_infections']
            self.local_7day_infections = data['local_7day_infections']

            return render_template('index.html',
                                   image=self.image,
                                   updates=self.updates,
                                   news_articles=self.news_articles,
                                   location=self.location,
                                   local_7day_infections=self.local_7day_infections,
                                   nation_location=self.nation_location,
                                   national_7day_infections=self.national_7day_infections)

        @app.route('/index')
        def index():
            """Returns the html template as an interactive dashboard on a local server"""
            response = request.args
            title = response.get("notif")
            update_title = response.get("update_item")
            update_box = response.get("update")
            label_box = response.get("two")
            repeat_box = response.get("repeat")
            covid_data_box = response.get("covid-data")
            news_box = response.get("news")

            if title is not None:
                for article in self.news_articles:
                    if article['title'] == title:
                        self.deleted_articles.append(article)
                        self.news_articles.remove(article)
                        logging.debug("Article removed")

            if update_title is not None:
                for update_item in self.updates:
                    if update_item['title'] == update_title:
                        self.updates.remove(update_item)
                        logging.debug("Update window removed")

            if update_box == "":

                if covid_data_box is not None:
                    self.local_covid_data_update()
                    self.national_covid_data_update()

                if news_box is not None:
                    self.news_update()

            elif update_box is not None and ":" in update_box:
                today = date.today().strftime('%d %m %y ')
                datetime_object = datetime.strptime(today + update_box, '%d %m %y %H:%M')

                if datetime_object < datetime.now():
                    datetime_object += timedelta(days=1)

                update_item = {'title': label_box, 'content': datetime_object}

                if update_item not in self.updates:
                    self.updates.append({'title': label_box, 'content': datetime_object})
                    logging.debug("Add update label and time to update tab")
                    self.scheduler.add_job(func=self.process_update,
                                           args=(label_box, repeat_box, covid_data_box, news_box, datetime_object),
                                           trigger="date",
                                           run_date=datetime_object)

                    logging.debug("Schedule update for specified time")

            return render_template('index.html',
                                   image=self.image,
                                   updates=self.updates,
                                   news_articles=self.news_articles,
                                   location=self.location,
                                   local_7day_infections=self.local_7day_infections,
                                   nation_location=self.nation_location,
                                   national_7day_infections=self.national_7day_infections)


        app.run(host="127.0.0.1", port=5000, debug=True)


