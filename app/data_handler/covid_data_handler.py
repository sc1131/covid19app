import os

from uk_covid19 import Cov19API
import json
import sched
import time
from app.defintions import ROOT_DIR

with open(os.path.join(ROOT_DIR,"config/config.json"), "r", encoding="utf-8") as config_file:
    # Open the configuration file and retrieve relevant settings
    CONFIG_DATA = json.load(config_file)
    COVID_DATA_FILTERS = [f'areaType={CONFIG_DATA["Covid Data Configuration"]["Location Type"]}',
                          f'areaName={CONFIG_DATA["Covid Data Configuration"]["Location"]}']
    OUTPUT_FORMAT = CONFIG_DATA["Covid Data Configuration"]["Output Format"]


def parse_csv_data(csv_filename):
    """Store data in csv file, line by line, in list"""
    file = open(csv_filename)
    # Store File info in list called Record
    record = []
    # Append each line of file to record
    for line in file:
        record.append(line.strip())
    file.close()
    return record


covid_csv_data = parse_csv_data(os.path.join(ROOT_DIR,"data_handler/nation_2021-10-28.csv"))


def process_covid_csv_data(covid_csv_data):
    """Finds current hospital cases, total deaths and cases in last seven days."""
    current_hospital_cases = 0
    total_deaths = 0
    last7days_cases = 0

    # Find hospital cases
    # Strip row of commas, check if hospital record exists
    first_row = covid_csv_data[1].split(',')
    if first_row[5].isnumeric():
        current_hospital_cases = int(first_row[5])
    else:
        raise Exception("Error, no hospital cases found")

    # Find total deaths
    # Ignore heading so start at index 1/second row
    # Strip row of commas and check for total deaths entry
    for row in covid_csv_data[1:]:
        data_entry = row.split(',')
        if not data_entry[4].isnumeric():
            # No entry here; check next row
            continue
            # Found Entry
        total_deaths = int(data_entry[4])
        break
        # Find cases in last seven days
        # Use count to keep track of recorded entries
    count = 0
    # Check each row for new cases entry
    for row in covid_csv_data[1:]:
        data_entry = row.split(',')
        if not data_entry[6].isnumeric():
            # No entry found
            continue
            # Increment data_handler to variable
        last7days_cases += int(data_entry[6])
        count += 1
        # Stop accumulating data_handler after seven days/entries
        if count == 7:
            break

    return last7days_cases, current_hospital_cases, total_deaths


process_covid_csv_data(covid_csv_data);


def covid_API_request(location="Exeter", location_type="ltla"):
    """Returns Json of Covid Information based on location and location type passed as arguments. Default
    arguments are location: "Exeter", location type:"ltla". See config file to change returned information """
    locale = [
        'areaName=' + location, 'areaType=' + location_type

    ]

    api = Cov19API(filters=locale, structure=OUTPUT_FORMAT)

    data = api.get_json()

    return data


# Create function with global variable, data_handler to provide updated info
def global_api_request():
    """Stores data returned by covid_API_request() in global variable, which can in turn be used in
    schedule_covid_updates function """
    global data
    data = covid_API_request()


def schedule_covid_updates(update_interval, update_name):
    """Returns covid information after specified period of time. Arguments include update interval in seconds and
    update name respectively"""
    timer = sched.scheduler(time.time, time.sleep)
    timer.enter(update_interval, 1, global_api_request, )
    timer.run()
    return data
