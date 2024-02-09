# Import the required libraries for Dash and Plotly
from dash import Dash
from dash import html as html
from dash import dcc as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import data_process
import numpy as np

app = Dash(__name__,external_stylesheets=[dbc.themes.ZEPHYR])

# Specifying the button group
button_groups = dbc.ButtonGroup(
    [dbc.Button("Learn More",href='https://www.who.int/emergencies/diseases/novel-coronavirus-2019'), dbc.Button("Github",href='https://github.com/ronanmccormack-ca/DAV2021-Mini-Project'), dbc.Button("Website",href='https://datahouse.ca')]
)

# App layout
app.layout = html.Div(id='parent', children=[
    html.H1(id='H1', children='COVID-19 Dashboard', style={'textAlign': 'center', \
                                                           'marginTop': 30, 'marginBottom': 30}),
    html.Div(children='''
        Created by Ronan Mc Cormack
    ''', style={
        'textAlign': 'center',
        'color': 'primary',
        'marginBottom': 10
    }),
    # The dropdown to selected which country you wish to view
    html.Div(id='cases_graph', children=[
        dbc.Row([
            button_groups
        ]),
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': i, 'value': i} for i in np.sort(data_process.get_locations())],
            value='Ireland',
            style={
                'width': '90%',
                'padding-left': '20%',
                'marginTop': 20
            }
        ),
    ]),
    # The cards which display the raw data
    html.Div(id='cards', children=[
        dbc.Row([
            dbc.Card([
                dbc.CardBody([
                    html.P("Total Cases", className='card-title'),
                    html.H5(id='total_cases', className='card-text'),
                ]),
            ], color="primary", outline=True,
                style={"marginTop": 20,
                       'width': '25%',
                       'textAlign': 'center'}),
            dbc.Card([
                dbc.CardBody([
                    html.P("Total Deaths", className='card-title'),
                    html.H5(id='total_deaths', className='card-text'),
                ]),
            ], color="primary", outline=True,
                style={"marginTop": 20,
                       'width': '25%',
                       'textAlign': 'center'}),
            dbc.Card([
                dbc.CardBody([
                    html.P("New Cases", className='card-title'),
                    html.H5(id='new_cases', className='card-text'),
                ]),
            ], color="primary", outline=True,
                style={"marginTop": 20,
                       'width': '25%',
                       'textAlign': 'center'}),
            dbc.Card([
                dbc.CardBody([
                    html.P("New Deaths", className='card-title'),
                    html.H5(id='new_deaths', className='card-text'),
                ]),
            ], color="primary", outline=True,
                style={"marginTop": 20,
                       'width': '25%',
                       'textAlign': 'center'}),
        ]),
    ]),
    # The Covid Graphs used in the dashboard
    html.Div(id='new_case_graph', children=[
        dcc.Graph(id='new_case_fig', style={'display': 'inline-block', 'width': '50%', "marginTop": 20, }),
        dcc.Graph(id='new_deaths_fig', style={'display': 'inline-block', 'width': '50%'})
    ]),
    html.Div(id='total_cases_graph', children=[
        dcc.Graph(id='top_country_fig', style={'display': 'inline-block', 'width': '50%'}),
        dcc.Graph(id='top_continent_fig', style={'display': 'inline-block', 'width': '50%'}),
    ]),
])

@app.callback(
    Output(component_id='total_cases', component_property='children'),
    (Output(component_id='total_deaths', component_property='children')),
    (Output(component_id='new_cases', component_property='children')),
    (Output(component_id='new_deaths', component_property='children')),
    (Output(component_id='new_case_fig',component_property='figure')),
    (Output(component_id='new_deaths_fig',component_property='figure')),
    (Output(component_id='top_country_fig',component_property='figure')),
    (Output(component_id='top_continent_fig',component_property='figure')),
    [Input(component_id='dropdown', component_property='value')]
)
def update_output(dropdown_value):
    df = data_process.process_data(dropdown_value)

    # Find the maximum value in the 'total_cases' column
    total_cases = df['new_cases'].sum()

    # Find the maximum value in the 'total_deaths' column
    total_deaths = df['new_deaths'].sum()

    # Find the recent value in the 'new_cases' column
    new_cases = df['new_cases'].iloc[-1]

    # Find the recent value in the 'new_deaths' column
    new_deaths = df['new_deaths'].iloc[-1]

    # Format the numbers with commas
    total_cases = "{:,}".format(total_cases)
    total_deaths = "{:,}".format(total_deaths)
    new_cases = "{:,}".format(new_cases)
    new_deaths = "{:,}".format(new_deaths)

    new_cases_fig = go.Figure()
    new_cases_fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['total_cases'],
        mode='lines',
        name='Total Cases',
        line=dict(color='black', width=1)
    ))

    new_cases_fig.update_layout(
        title={'text': 'Total Cases ' + dropdown_value, 'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
        xaxis_title='Date',
        yaxis_title='Confirmed Cases'
    )

    new_deaths_fig = go.Figure()
    new_deaths_fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['total_deaths'],
        mode='lines',
        name='Total Deaths',
        line=dict(color='red', width=1)
    ))

    new_deaths_fig.update_layout(
        title={'text': 'Total Deaths ' + dropdown_value, 'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
        xaxis_title='Date',
        yaxis_title='Confirmed Deaths'
    )
    top_case_country = list(df.groupby('location').max().sort_values(by='total_cases', ascending=False).reset_index().head()[
        'location'])
    top_case_country.append(dropdown_value)
    top_country_fig = go.Figure()
    for country in set(top_case_country):
        temp_df = df[df['location'] == country]
        top_country_fig.add_trace(go.Scatter(x=temp_df['date'], y=temp_df['total_cases'], \
                                  name=country, ))

    top_country_fig.update_layout(title={'text': '{}'.format(dropdown_value) + ' Compared to Top 5 Countries - Total Cases',
                              'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
                       xaxis_title='Date',
                       yaxis_title='Total Cases',
                       )
    top_con = df.groupby(['date', 'continent']).sum().reset_index()
    top_continent_fig = go.Figure()
    for continent in set(top_con['continent'].unique()):
        temp_df = top_con[top_con['continent'] == continent]
        top_continent_fig.add_trace(go.Scatter(x=temp_df['date'], y=temp_df['total_cases'], \
                                             name=continent, ))

    top_continent_fig.update_layout(
        title={'text':'Total Cases by Continent',
               'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
        xaxis_title='Date',
        yaxis_title='Total Cases',
        )

    # Return the result to be displayed in the output component
    return total_cases,total_deaths, new_cases, new_deaths, new_cases_fig, new_deaths_fig, top_country_fig, top_continent_fig

if __name__ == '__main__':
    app.run_server()