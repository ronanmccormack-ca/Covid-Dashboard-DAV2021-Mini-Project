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

def get_vac(df):
    vac_df_max = pd.DataFrame(columns=df.columns)
    for location in df['location'].unique():
        result = df.loc[(df['location'] == location) & (
                    df['date'] == df.loc[(df['location'] == location)]['date'].max())]
        vac_df_max = pd.concat((vac_df_max, result))
    vac_df_max = vac_df_max.fillna(0)
    vac_df_max['date'] = pd.to_datetime(vac_df_max['date'])
    date = vac_df_max['date'].max()
    vac_cols = [x for x in vac_df_max.columns[7::]]
    vac_cols.append('iso_code')
    vac_cols.append('date')
    vac_cols.append('total_vaccinations')
    vac_df_max = vac_df_max.drop(columns=vac_cols)
    vac_df_max = vac_df_max.set_index('location').T
    vac_df_max = vac_df_max.astype(int)
    vac_df_max = vac_df_max.rename(index={'people_vaccinated': "People Vaccinated",
                                          'people_fully_vaccinated': "People Fully Vaccinated",
                                          'total_boosters': "Total Boosters"})
    return vac_df_max
