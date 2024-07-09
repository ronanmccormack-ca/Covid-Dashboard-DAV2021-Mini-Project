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
server = app.server

# Specifying the button group
button_groups = dbc.ButtonGroup(
    [
        dbc.Button("Learn More", href='https://www.who.int/emergencies/diseases/novel-coronavirus-2019',
                   className="me-1 btn-lg"),
        dbc.Button("Github", href='https://github.com/ronanmccormack-ca/DAV2021-Mini-Project', className="me-1 btn-lg"),
        dbc.Button("Website", href='https://datahouse.ca', className="btn-lg")
    ],
    className="d-flex justify-content-center mb-3",  # Flexbox for centering and margin-bottom
    size="lg",  # Make the buttons larger
)

# App layout
app.layout = html.Div(id='parent', children=[
    html.H1(id='H1', children='COVID-19 Dashboard', className='text-center mt-4 mb-4'),
    html.Div(children='Created by Ronan Mc Cormack', className='text-center text-primary mb-2'),

    # Include the button group in the layout
    dbc.Container(
        dbc.Row(
            dbc.Col(button_groups, width=12),
            justify='center'  # Horizontally center the ButtonGroup in the row
        ),
        fluid=True
    ),
    # The dropdown to selected which country you wish to view
    html.Div(id='cases_graph', children=[
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='dropdown',
                    options=[{'label': i, 'value': i} for i in data_process.get_locations()],
                    value='Canada',
                ), width=10, lg=6, md=8, className="my-3 mx-auto"  # Adjusted for responsiveness
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='date_dropdown',
                    options=[{'label': i, 'value': i} for i in data_process.get_dates()],
                    value=max(data_process.get_dates()) if data_process.get_dates() else None
                ), width=10, lg=6, md=8, className="my-3 mx-auto"  # Adjusted for responsiveness
            )
        ])
    ]),
    html.Div(id='cards', children=[
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.P("Total Cases", className='card-title text-center'),
                        html.H5(id='total_cases', className='card-text text-center'),
                    ]),
                ], color="primary", outline=True),
                width=12, lg=3, className='mb-4'
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.P("Total Deaths", className='card-title text-center'),
                        html.H5(id='total_deaths', className='card-text text-center'),
                    ]),
                ], color="primary", outline=True),
                width=12, lg=3, className='mb-4'
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.P("New Cases", className='card-title text-center'),
                        html.H5(id='new_cases', className='card-text text-center'),
                    ]),
                ], color="primary", outline=True),
                width=12, lg=3, className='mb-4'
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.P("New Deaths", className='card-title text-center'),
                        html.H5(id='new_deaths', className='card-text text-center'),
                    ]),
                ], color="primary", outline=True),
                width=12, lg=3, className='mb-4'
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.P("Total Vaccinations", className='card-title text-center'),
                        html.H5(id='total_pop_vac', className='card-text text-center'),
                    ]),
                ], color="primary", outline=True),
                width=12, lg=3, className='mb-4'
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.P("People Fully Vaccinated", className='card-title text-center'),
                        html.H5(id='total_full_vac', className='card-text text-center'),
                    ]),
                ], color="primary", outline=True),
                width=12, lg=3, className='mb-4'
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.P("People Vaccinated", className='card-title text-center'),
                        html.H5(id='total_vac', className='card-text text-center'),
                    ]),
                ], color="primary", outline=True),
                width=12, lg=3, className='mb-4'
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.P("Total Boosters", className='card-title text-center'),
                        html.H5(id='total_boost', className='card-text text-center'),
                    ]),
                ], color="primary", outline=True),
                width=12, lg=3, className='mb-4'
            ),
        ]),
    ]),
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(id='new_case_fig'), width=12, lg=6),
            dbc.Col(dcc.Graph(id='new_deaths_fig'), width=12, lg=6)
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='total_case_fig'), width=12, lg=6),
            dbc.Col(dcc.Graph(id='total_deaths_fig'), width=12, lg=6)
        ])
    ])
])

@app.callback(
    Output(component_id='total_cases', component_property='children'),
    (Output(component_id='total_deaths', component_property='children')),
    (Output(component_id='new_cases', component_property='children')),
    (Output(component_id='new_deaths', component_property='children')),
    (Output(component_id='total_pop_vac', component_property='children')),
    (Output(component_id='total_full_vac', component_property='children')),
    (Output(component_id='total_vac', component_property='children')),
    (Output(component_id='total_boost', component_property='children')),
    (Output(component_id='new_case_fig',component_property='figure')),
    (Output(component_id='new_deaths_fig',component_property='figure')),
    (Output(component_id='total_case_fig',component_property='figure')),
    (Output(component_id='total_deaths_fig',component_property='figure')),
    [Input(component_id='dropdown', component_property='value'),
    Input(component_id='date_dropdown', component_property='value')]
)
def update_output(dropdown_value, dropdown_date):
    df = data_process.get_country_data(dropdown_value,dropdown_date)

    # Find the maximum value in the 'total_cases' column
    total_cases = df['new_cases'].sum()

    # Find the maximum value in the 'total_deaths' column
    total_deaths = df['new_deaths'].sum()

    # Find the recent value in the 'new_cases' column
    new_cases = df['new_cases'].iloc[-1]

    # Find the recent value in the 'new_deaths' column
    new_deaths = df['new_deaths'].iloc[-1]

    # Find the recent value in the 'total_vaccinations' column
    total_pop_vac = df['total_vaccinations'].iloc[-1]

    # Find the recent value in the 'people_fully_vaccinated' column
    total_full_vac = df['people_fully_vaccinated'].iloc[-1]

    # Find the recent value in the 'people_vaccinated' column
    total_vac = df['people_vaccinated'].iloc[-1]

    # Find the recent value in the 'total_boosters' column
    total_boost = df['total_boosters'].iloc[-1]

    # Format the numbers with commas
    total_cases = "{:,}".format(total_cases)
    total_deaths = "{:,}".format(total_deaths)
    new_cases = "{:,}".format(new_cases)
    new_deaths = "{:,}".format(new_deaths)
    total_pop_vac = "{:,}".format(total_pop_vac)
    total_full_vac = "{:,}".format(total_full_vac)
    total_vac = "{:,}".format(total_vac)
    total_boost = "{:,}".format(total_boost)

    new_cases_fig = go.Figure()
    new_cases_fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['new_cases'],
        mode='lines',
        name='New Cases',
        line=dict(color='black', width=2)
    ))

    new_cases_fig.update_layout(
        title={'text': 'New Cases ' + dropdown_value, 'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
        xaxis_title='Date',
        yaxis_title='Confirmed New Cases'
    )

    new_deaths_fig = go.Figure()
    new_deaths_fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['new_deaths'],
        mode='lines',
        name='New Deaths',
        line=dict(color='red', width=2)
    ))

    new_deaths_fig.update_layout(
        title={'text': 'New Deaths ' + dropdown_value, 'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
        xaxis_title='Date',
        yaxis_title='Confirmed New Deaths'
    )

    total_cases_fig = go.Figure()
    total_cases_fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['total_cases'],
        mode='lines',
        name='Total Cases',
        line=dict(color='blue', width=2)
    ))

    total_cases_fig.update_layout(
        title={'text': 'Total Cases ' + dropdown_value, 'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
        xaxis_title='Date',
        yaxis_title='Total Cases'
    )

    total_deaths_fig = go.Figure()
    total_deaths_fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['total_deaths'],
        mode='lines',
        name='Total Deaths',
        line=dict(color='orange', width=2)
    ))

    total_deaths_fig.update_layout(
        title={'text': 'Total Deaths ' + dropdown_value, 'y': 0.9, 'x': 0.5, 'yanchor': 'top'},
        xaxis_title='Date',
        yaxis_title='Total Deaths'
    )
    # Return the result to be displayed in the output component
    return total_cases, total_deaths, new_cases, new_deaths, total_pop_vac, total_full_vac, total_vac, total_boost, new_cases_fig, new_deaths_fig, total_cases_fig, total_deaths_fig

if __name__ == '__main__':
    app.run_server()
