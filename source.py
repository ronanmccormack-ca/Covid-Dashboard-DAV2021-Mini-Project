import pandas as pd

def source_data():
    info_url ='https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv'
    df = pd.read_csv(info_url)
    return df
