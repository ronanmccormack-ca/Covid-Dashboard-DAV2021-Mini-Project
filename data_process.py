import pandas as pd
import numpy as np

def process_data():
    # Specify the dataset URL
    info_url = 'https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv'

    # Read the dataset into a DataFrame
    df = pd.read_csv(info_url)

    # Extract Columns for Visualization
    df = df[['continent', 'location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']]

    # Specify the continents
    continents_location = df[df['continent'].isna()]['location'].unique()

    # Loop over each continent and drop it from the DataFrame
    for x in continents_location:
        df = df.drop(df[df.location == x].index)

    df = df.fillna(0)

    # Converting floats to integers
    for x in df.select_dtypes(float).columns:
        df[x] = df[x].astype(int)

    # Converting the column 'date' to datetime
    df['date'] = pd.to_datetime(df['date'])

    df = df.groupby(['continent','location','date']).sum().reset_index()

    return df