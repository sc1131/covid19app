import os

import pytest
from app.defintions import*

from app.data_handler.covid_data_handler import parse_csv_data
from app.data_handler.covid_data_handler import process_covid_csv_data
from app.data_handler.covid_data_handler import covid_API_request
from app.data_handler.covid_data_handler import schedule_covid_updates

print(os.path.abspath(__file__))


# Test Passed
def test_parse_csv_data():
    """Checks parse_csv_data function by verifying length of csv file"""
    data = parse_csv_data(os.path.join(ROOT_DIR,'news_handler/nation_2021-10-28.csv'))
    assert len(data) == 639


# Test failed as 240299 cases in total number of cases in last eight days (20-27th October)
# Total number of cases in last seven days is actually 206057 (21st-27th October)
# Test passes with this number

def test_process_covid_csv_data():
    """Checks process_covid_csv_data by cross-checking return values with figures calculated manually. Total number
    of cases in last seven days is actually 206057 (21st-27th October) Test passes with this number."""
    last7days_cases, current_hospital_cases, total_deaths = \
        process_covid_csv_data(parse_csv_data(os.path.join(ROOT_DIR,'news_handler/nation_2021-10-28.csv')))
    assert last7days_cases == 206_057  # Amended from 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544


# Test passed; return type is a dictionary
def test_covid_API_request():
    """Checks that covid_API_request returns a dictionary"""
    data = covid_API_request()
    assert isinstance(data, dict)


# Test passed
def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=10, update_name='update test')


if __name__ == 'main':
    pytest.main()
