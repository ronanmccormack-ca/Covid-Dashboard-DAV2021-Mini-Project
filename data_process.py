import pandas as pd
import requests

def get_country_data(country_name, query_date):
    # Construct the URL with an optional date query parameter
    url = f'https://covidapi-zm9v.onrender.com/v1/country/{country_name}?date={query_date}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        data = pd.DataFrame(data)
        data['date'] = pd.to_datetime(data['date']).dt.date
        data = data.sort_values(by='date', ascending=True)
        return data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return pd.DataFrame()  # Return an empty DataFrame in case of failure

def get_locations():
    url = 'https://covidapi-zm9v.onrender.com/v1/countries'
    response = requests.get(url)

    if response.status_code == 200:
        countries_data = response.json()  # This should be a list of dictionaries
        country_names = [country['name'] for country in countries_data]  # Extracting country names into a list
        return country_names
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

def get_dates():
    url = 'https://covidapi-zm9v.onrender.com/v1/dates'
    response = requests.get(url)

    if response.status_code == 200:
        dates_data = response.json()
        dates_data = pd.DataFrame(dates_data)
        dates_data = pd.to_datetime(dates_data['date']).dt.date
        return dates_data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []