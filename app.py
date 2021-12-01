
import numpy as np
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output
from dash import State,html
import plotly
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import datetime
from datetime import date

info_url ='https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv'

df = pd.read_csv(info_url)

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

def get_world(col):
    today = date.today()

    yesterday = today - datetime.timedelta(days=1)

    continent_cases = df[df['date'] == yesterday.strftime('%Y%m%d')]

    total_cases_world = pd.DataFrame(continent_cases.groupby('continent')[col].sum())

    return total_cases_world

df = clean_df(df)

deaths = get_col(df,'total_deaths')
cases = get_col(df,'total_cases')
new_cases = get_col(df,'new_cases')
new_deaths = get_col(df,'new_deaths')

total_cases_world = get_world('total_cases')
new_cases_world = get_world('new_cases')

button_group = dbc.ButtonGroup(
    [dbc.Button("Learn More",href='https://www.who.int/emergencies/diseases/novel-coronavirus-2019'), dbc.Button("Github",href='https://ronanmccormack.ca')]
)

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SKETCHY])
server = app.server

loc_columns = [x for x in df['location'].unique()]

app.layout = html.Div(id='parent', children=[
    html.H1(id='H1', children='COVID-19 Dashboard', style={'textAlign': 'center', \
                                                           'marginTop': 30, 'marginBottom': 30}),
    html.Div(children='''
        Created by Ronan McCormack S00144576
    ''', style={
        'textAlign': 'center',
        'color': 'primary',
        'marginBottom': 10
    }),

    html.Div(id='cases_graph', children=[
        dbc.Row([
            button_group
        ]),
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': i, 'value': i} for i in loc_columns],
            value='Ireland',
            style={
                'width': '90%',
                'padding-left': '20%',
                'marginTop': 40
            }
        ),
        dcc.Graph(id='cases_plot', style={'display': 'inline-block', 'width': '50%'}),
        dcc.Graph(id='death_plot', style={'display': 'inline-block', 'width': '50%'}),
    ]),
    html.Div(id='new_case_graph', children=[
        dcc.Graph(id='new_case_plot', style={'display': 'inline-block', 'width': '50%'}),
        dcc.Graph(id='new_death_plot', style={'display': 'inline-block', 'width': '50%'})
    ]),
    html.Div(id='vac_graph', children=[
        dcc.Graph(id='total_world_plot', style={'display': 'inline-block', 'width': '50%'}),
        dcc.Graph(id='new_world_plot', style={'display': 'inline-block', 'width': '50%'})
    ]),
])


## App Callbacks
@app.callback(Output(component_id='cases_plot', component_property='figure'),
              (Output(component_id='death_plot', component_property='figure')),
              (Output(component_id='new_case_plot', component_property='figure')),
              (Output(component_id='new_death_plot', component_property='figure')),
              (Output(component_id='total_world_plot', component_property='figure')),
              (Output(component_id='new_world_plot', component_property='figure')),
              [Input(component_id='dropdown', component_property='value')])
def cases_update(dropdown_value):
    fig = go.Figure([go.Scatter(x=cases.index, y=cases['{}'.format(dropdown_value)], \
                                line=dict(color='black', width=4))
                     ])

    fig.update_layout(title={'text': 'Confirmed Cases',
                             'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
                      xaxis_title='Date',
                      yaxis_title='Confirmed Cases'
                      )

    fig1 = go.Figure([go.Scatter(x=deaths.index, y=deaths['{}'.format(dropdown_value)], \
                                 line=dict(color='black', width=4))
                      ])

    fig1.update_layout(title={'text': 'Confirmed Deaths',
                              'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
                       xaxis_title='Date',
                       yaxis_title='Confirmed Deaths'
                       )

    fig2 = go.Figure([go.Bar(x=new_cases.index, y=new_cases['{}'.format(dropdown_value)], \
                             marker=dict(color='black'))
                      ])

    fig2.update_layout(title={'text': 'New Cases',
                              'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
                       xaxis_title='Date',
                       yaxis_title='Confirmed New Cases',
                       )
    fig3 = go.Figure([go.Bar(x=new_deaths.index, y=new_deaths['{}'.format(dropdown_value)], \
                             marker=dict(color='black'))
                      ])

    fig3.update_layout(title={'text': 'New Deaths',
                              'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
                       xaxis_title='Date',
                       yaxis_title='Confirmed New Deaths'
                       )
    fig4 = go.Figure([go.Bar(x=total_cases_world.index, y=total_cases_world['total_cases'], \
                             marker=dict(color='black'))
                      ])

    fig4.update_layout(title={'text': 'Total COVID Cases Per Continent',
                              'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
                       xaxis_title='Continent',
                       yaxis_title='Total Cases'
                       )
    fig5 = go.Figure([go.Bar(x=new_cases_world.index, y=new_cases_world['new_cases'], \
                             marker=dict(color='black'))
                      ])

    fig5.update_layout(title={'text': 'Total New COVID Cases Per Continent',
                              'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
                       xaxis_title='Continent',
                       yaxis_title='Total Cases'
                       )
    return fig, fig1, fig2, fig3, fig4, fig5

if __name__ == '__main__':
    app.run_server(host='localhost',port='8000')
