
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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])
server = app.server

loc_columns = [x for x in df['location'].unique()]
night_colors = ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)',
                'rgb(36, 55, 57)', 'rgb(6, 4, 4)']
irises_colors = ['rgb(33, 75, 99)', 'rgb(79, 129, 102)', 'rgb(151, 179, 100)',
                 'rgb(175, 49, 35)', 'rgb(36, 73, 147)']
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
                'marginTop': 40
            }
        ),
    ]),
    html.Div(id='new_case_graph', children=[
        dcc.Graph(id='cases_plot', style={'display': 'inline-block', 'width': '50%'}),
        dcc.Graph(id='new_case_plot', style={'display': 'inline-block', 'width': '50%'})
    ]),
    dbc.Container([
        dcc.Graph(id='top_country_plot', style={'display': 'inline-block', 'width': '99%'}),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in top_cases_country],
            data=cases.iloc[-1:].to_dict('records'),
        ),
    ]),
    html.Div(id='vac_graph', children=[
        dcc.Graph(id='new_world_plot', style={'display': 'inline-block', 'width': '50%'}),
        dcc.Graph(id='total_world_plot', style={'display': 'inline-block', 'width': '50%'})
    ]),
])


## App Callbacks
@app.callback(Output(component_id='cases_plot', component_property='figure'),
              (Output(component_id='new_case_plot', component_property='figure')),
              (Output(component_id='total_world_plot', component_property='figure')),
              (Output(component_id='new_world_plot', component_property='figure')),
              (Output(component_id='top_country_plot', component_property='figure')),
              [Input(component_id='dropdown', component_property='value')])
def cases_update(dropdown_value):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=cases.index, y=cases['{}'.format(dropdown_value)], mode='lines', name='Total Cases',
                             line=dict(color='black', width=4)))
    fig.add_trace(go.Scatter(x=deaths.index, y=deaths['{}'.format(dropdown_value)], mode='lines', name='Total Deaths',
                             line=dict(color='red', width=4)))
    fig.update_layout(title={'text': 'Total Cases & Deaths',
                             'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
                      xaxis_title='Date',
                      yaxis_title='Confirmed Cases & Deaths'
                      )
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=new_cases.index, y=new_cases['{}'.format(dropdown_value)], name='New Cases',
                          marker=dict(color='black')))
    fig2.add_trace(go.Bar(x=new_deaths.index, y=new_deaths['{}'.format(dropdown_value)], name='New Deaths',
                          marker=dict(color='red')))
    fig2.update_layout(title={'text': 'New Cases & Deaths',
                              'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
                       xaxis_title='Date',
                       yaxis_title='Confirmed New Cases',
                       )
    fig4 = go.Figure([go.Bar(x=total_cases_world.index, y=total_cases_world['total_cases'],
                             marker_color=irises_colors)
                      ])

    fig4.update_layout(title={'text': 'Total COVID Cases Per Continent'}
                       )
    fig5 = go.Figure([go.Pie(labels=vac_df.index, values=vac_df['{}'.format(dropdown_value)],
                             hole=.3, marker_colors=night_colors)
                      ])

    fig5.update_layout(title={'text': 'Percentage of All People Vaccinationed in ' + '{}'.format(dropdown_value)}
                       )
    top_cases_country.append('{}'.format(dropdown_value))
    fig6 = go.Figure()
    for country in top_cases_country:
        fig6.add_trace(go.Scatter(x=cases.index, y=cases[country], name=country, ))

    fig6.update_layout(title={'text': '{}'.format(dropdown_value) + ' Compared to Top 5 Countries - Total Cases',
                              'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
                       xaxis_title='Date',
                       yaxis_title='Confirmed New Cases',
                       )

    return fig, fig2, fig4, fig5, fig6
if __name__ == '__main__':
    app.run_server()
