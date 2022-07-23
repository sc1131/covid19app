import pytest

from app.news_handler.covid_news_handling import news_API_request
from app.news_handler.covid_news_handling import update_news


def test_news_API_request():
    assert news_API_request()
    # assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()


def test_update_news():
    assert update_news()


if __name__ == 'main':
    pytest.main()
