import pandas as pd
def process_data(country):
    # Initialize an empty DataFrame to store the concatenated results
    df = pd.DataFrame()

    # Process the data in chunks
    for chunk in pd.read_csv('https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv', chunksize=10000,
                             usecols=['continent', 'location', 'date', 'total_cases', 'new_cases', 'total_deaths',
                                      'new_deaths']):
        # Apply the same processing as in your original function
        chunk = chunk[chunk['location'] == country]
        chunk.fillna(0, inplace=True)

        # Converting floats to integers
        for x in chunk.select_dtypes(float).columns:
            chunk[x] = chunk[x].astype('int32')

        # Convert 'date' to datetime
        chunk['date'] = pd.to_datetime(chunk['date'])

        # Concatenate the processed chunk with the final DataFrame
        df = pd.concat([df, chunk], ignore_index=True)

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