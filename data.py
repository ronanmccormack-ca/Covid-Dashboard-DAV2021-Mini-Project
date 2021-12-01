import numpy as np
import pandas as pd
import datetime
from datetime import date

def clean_df(df):
    continents_location = df[df['continent'].isna()]['location'].unique()
    for x in continents_location:
        df = df.drop(df[df.location==x].index)
    df = df.fillna(0)
    drop_cols=['iso_code','tests_units']
    df = df.drop(columns=drop_cols)
    for x in df.select_dtypes(float).columns:
        df[x] = df[x].astype(int)
    df['date'] = pd.to_datetime(df['date'])
    return df

def get_col(df, column):
    ## Get the subset df to work off
    cases = df[['location', 'date', column]]

    ## Create the dates variable and sort it
    dates = cases['date'].unique()
    dates.sort()

    ## Get the len of dates
    len_dates = len(dates)

    ## Get the unique locations
    locations = [x for x in cases['location'].unique()]

    data = list()
    ## Loop through each location to get the column and merge it to the dataframe
    for x in locations:
        y = ()
        len_y = 0
        y = list(cases[cases['location'] == x][column])
        len_y = len(y)
        len_zeroes = len_dates - len_y
        zeroes = list(np.zeros(len_zeroes))
        merge = zeroes + y
        data.append(merge)
    data = np.array(data).T
    df2 = pd.DataFrame(data, columns=locations, index=dates)
    df2 = df2.astype(int)

    return df2

def get_world(df,col):
    today = date.today()

    yesterday = today - datetime.timedelta(days=1)

    continent_cases = df[df['date'] == yesterday.strftime('%Y%m%d')]

    total_cases_world = pd.DataFrame(continent_cases.groupby('continent')[col].sum())

    return total_cases_world