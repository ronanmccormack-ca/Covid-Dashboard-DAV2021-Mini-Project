
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
import data

info_url ='https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv'
df = pd.read_csv(info_url)

df = data.clean_df(df)
deaths = data.get_col(df,'total_deaths')
cases = data.get_col(df,'total_cases')
new_cases = data.get_col(df,'new_cases')
new_deaths = data.get_col(df,'new_deaths')

total_cases_world = data.get_world(df,'total_cases')
new_cases_world = data.get_world(df,'new_cases')

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
    app.run_server()
