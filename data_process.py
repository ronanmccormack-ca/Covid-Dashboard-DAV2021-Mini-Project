import pandas as pd
import requests

def get_country_data(country_name):
    url = f'https://covidapi-zm9v.onrender.com/v1/country/{country_name}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)
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