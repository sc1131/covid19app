from datetime import datetime

import pytest
from app.Flask import CovidApp


app = CovidApp()


def test_local_covid_data_update():
    """Checks that local covid info is updated and stored in "local_7day_infections" field """
    app.local_covid_data_update()
    assert app.local_7day_infections > 0
    assert app.location == 'Exeter'


def test_national_covid_data_update():
    """Checks that national covid info is updated and stored in "national_7day_infections" field """
    app.national_covid_data_update()
    assert app.national_7day_infections > 0
    assert app.nation_location == 'England'


def test_news_update():
    """Checks that news is updated and stored in news_articles field"""
    app.news_update()
    assert len(app.news_articles) > 0


def test_process_update():
    """Checks that updates are processed properly"""
    time = datetime.now()
    app.updates.append({'title': 'test', 'content': time})
    app.process_update('test', None, 'covid-data_handler', 'news', time)
    assert len(app.updates) == 0


if __name__ == 'main':
    pytest.main()
