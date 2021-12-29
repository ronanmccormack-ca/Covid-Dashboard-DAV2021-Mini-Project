
import numpy as np
import pandas as pd
import dash
from dash import dash_table
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
vac_url = 'https://github.com/owid/covid-19-data/raw/master/public/data/vaccinations/vaccinations.csv'
vac_df = pd.read_csv(vac_url)
df = pd.read_csv(info_url)

df = data.clean_df(df)

deaths = data.get_col(df, 'total_deaths')
cases = data.get_col(df, 'total_cases')
new_cases = data.get_col(df, 'new_cases')
new_deaths = data.get_col(df, 'new_deaths')

total_cases_world = data.get_world(df, 'total_cases')
new_cases_world = data.get_world(df, 'new_cases')

vac_df = data.get_vac(vac_df)
button_group = dbc.ButtonGroup(
    [dbc.Button("Learn More", href='https://www.who.int/emergencies/diseases/novel-coronavirus-2019'),
     dbc.Button("Github", href='https://github.com/ronanmccormack-ca/DAV2021-Mini-Project')]
)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR])
server = app.server

loc_columns = [x for x in df['location'].unique()]
night_colors = ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)',
                'rgb(36, 55, 57)', 'rgb(6, 4, 4)']
top_cases_country = [x for x in
                     df[df['date'] == df['date'].max()].sort_values(by='total_cases', ascending=False)['location'].head(
                         5)]

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
                'marginTop': 20
            }
        ),
    ]),
    html.Div(id='cards', children=[
        dbc.Row([
            dbc.Card([
                dbc.CardBody([
                    html.P("Total Cases", className='card-title'),
                    html.H5(id='cases_card', className='card-text'),
                ]),
            ], color="primary", outline=True,
                style={"marginTop": 20,
                       'width': '25%',
                       'textAlign': 'center'}),
            dbc.Card([
                dbc.CardBody([
                    html.P("Total Deaths", className='card-title'),
                    html.H5(id='deaths_card', className='card-text'),
                ]),
            ], color="primary", outline=True,
                style={"marginTop": 20,
                       'width': '25%',
                       'textAlign': 'center'}),
            dbc.Card([
                dbc.CardBody([
                    html.P("New Cases", className='card-title'),
                    html.H5(id='new_cases_card', className='card-text'),
                ]),
            ], color="primary", outline=True,
                style={"marginTop": 20,
                       'width': '25%',
                       'textAlign': 'center'}),
            dbc.Card([
                dbc.CardBody([
                    html.P("New Deaths", className='card-title'),
                    html.H5(id='new_deaths_card', className='card-text'),
                ]),
            ], color="primary", outline=True,
                style={"marginTop": 20,
                       'width': '25%',
                       'textAlign': 'center'}),
        ]),
    ]),
    html.Div(id='new_case_graph', children=[
        dcc.Graph(id='cases_plot', style={'display': 'inline-block', 'width': '50%', "marginTop": 20, }),
        dcc.Graph(id='new_case_plot', style={'display': 'inline-block', 'width': '50%'})
    ]),
    dbc.Container([
        dcc.Graph(id='top_country_plot', style={'display': 'inline-block', 'width': '100%'}),
    ]),
    html.Div(id='vac_graph', children=[
        dcc.Graph(id='new_world_plot', style={'display': 'inline-block', 'width': '50%'}),
        dcc.Graph(id='total_world_plot', style={'display': 'inline-block', 'width': '50%'}),
    ]),
])


## App Callbacks
@app.callback(Output(component_id='cases_plot', component_property='figure'),
              (Output(component_id='new_case_plot', component_property='figure')),
              (Output(component_id='total_world_plot', component_property='figure')),
              (Output(component_id='new_world_plot', component_property='figure')),
              (Output(component_id='top_country_plot', component_property='figure')),
              (Output(component_id='cases_card', component_property='children')),
              (Output(component_id='deaths_card', component_property='children')),
              (Output(component_id='new_cases_card', component_property='children')),
              (Output(component_id='new_deaths_card', component_property='children')),
              [Input(component_id='dropdown', component_property='value')])
def cases_update(dropdown_value):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=cases.index, y=cases['{}'.format(dropdown_value)], mode='lines', name='Total Cases',
                             line=dict(color='black', width=4)))
    fig.add_trace(go.Scatter(x=deaths.index, y=deaths['{}'.format(dropdown_value)], mode='lines', name='Total Deaths',
                             line=dict(color='blue', width=4)))
    fig.update_layout(title={'text': 'Total Cases & Deaths',
                             'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
                      xaxis_title='Date',
                      yaxis_title='Confirmed Cases & Deaths'
                      )
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=new_cases.index, y=new_cases['{}'.format(dropdown_value)], name='New Cases',
                          marker=dict(color='black')))
    fig2.add_trace(go.Bar(x=new_deaths.index, y=new_deaths['{}'.format(dropdown_value)], name='New Deaths',
                          marker=dict(color='blue')))
    fig2.update_layout(title={'text': 'New Cases & Deaths',
                              'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
                       xaxis_title='Date',
                       yaxis_title='Confirmed New Cases',
                       )
    fig4 = go.Figure([go.Bar(x=total_cases_world.index, y=total_cases_world['total_cases'],
                             marker_color=night_colors)
                      ])

    fig4.update_layout(title={'text': 'Total COVID Cases Per Continent',
                              'y': 0.9, 'x': 0.5, 'yanchor': 'top'}
                       )
    fig5 = go.Figure([go.Pie(labels=vac_df.index, values=vac_df['{}'.format(dropdown_value)],
                             hole=.3, marker_colors=night_colors)
                      ])

    fig5.update_layout(title={'text': 'Percentage of All People Vaccinationed in ' + '{}'.format(dropdown_value),
                              'y': 0.9, 'x': 0.5, 'yanchor': 'top'}
                       )
    top_cases_country.append('{}'.format(dropdown_value))
    fig6 = go.Figure()
    for country in set(top_cases_country):
        fig6.add_trace(go.Scatter(x=cases.index, y=cases[country], name=country, ))

    fig6.update_layout(title={'text': '{}'.format(dropdown_value) + ' Compared to Top 5 Countries - Total Cases',
                              'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
                       xaxis_title='Date',
                       yaxis_title='Confirmed New Cases',
                       )
    cases_format = cases['{}'.format(dropdown_value)].iloc[-1]
    deaths_format = deaths['{}'.format(dropdown_value)].iloc[-1]
    new_cases_format = new_cases['{}'.format(dropdown_value)].iloc[-1]
    new_deaths_format = new_deaths['{}'.format(dropdown_value)].iloc[-1]
    return fig, fig2, fig4, fig5, fig6, cases_format, deaths_format, new_cases_format, new_deaths_format


if __name__ == '__main__':
    app.run_server()
