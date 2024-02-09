import pandas as pd

def process_data(country):
    # Read the dataset into a DataFrame
    df = pd.read_csv('https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv',usecols=['continent', 'location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths'])

    # Filter for the specific country as soon as possible
    df = df[df['location'] == country]

    # Fill missing values
    df.fillna(0, inplace=True)

    # Converting floats to integers
    for x in df.select_dtypes(float).columns:
        df[x] = df[x].astype('int32')

    # Converting the column 'date' to datetime
    df['date'] = pd.to_datetime(df['date'])

    return df

def get_locations():
    # Specify the dataset URL
    info_url = 'https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv'

    # Read the dataset into a DataFrame
    df = pd.read_csv(info_url)

    # Extract Columns for Visualization
    df = df[['continent', 'location']]

    # Specify the continents
    continents_location = df[df['continent'].isna()]['location'].unique()

    # Loop over each continent and drop it from the DataFrame
    for x in continents_location:
        df = df.drop(df[df.location == x].index)

    return df['location'].unique()