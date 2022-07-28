# Covid Dashboard

Covid Dashboard implements a simple personalised covid dashboard, which co-ordinates information about the COVID infection rates from the 
[_Public Health England API_](https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/) and news 
stories about Covid from [_News API_](https://newsapi.org/). 
The application runs continuously and responds to events, including Covid and news updates, triggered by user inputs.
The program also includes News and Data handling modules to deal with information pertaining to Covid-19. 

## Installation Guide

The [_Public Health England API_](https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/) and 
[_News API_](https://newsapi.org/) must be installed for the program to work.

To install the [_Public Health England API_](https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/):
```bash
pip install uk-covid19
```

To install the [_News API_](https://newsapi.org/):

```bash
pip install newsapi-python
```

Important Disclaimer: [_News API_](https://newsapi.org/) no longer works in the UK. Therefore a VPN must be used in 
order for the application to function. 

## Usage

In the app package:

- To run the data handling module, execute `covid_data_handler.py`

- To run the news handling module, execute `covid_news_handling.py`

To run the Covid Dashboard itself,  execute the `main.py` file in the project directory.

## Testing 

Run automated unit tests by running `tests` in the project directory.

Within `tests`, the news, data and dashboard modules can each be tested by running `test_covid_data_handler.py`, 
`test_news_data_handling.py` and `test_dashboard.py `respectively.










