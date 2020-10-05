# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H6('Interactive Master Plan Dashboard'),
    html.Div(['Starting Headcount: ',
        dcc.Input(id='initial-headcount', value='880', type='number')]),
    html.Label('Assumed to be 880 in 2019'),
    html.Br(),
    html.Div(['Anticipated Annual Growth: ',
        dcc.Slider(
            id='anticipated-annual-growth',
            dots=True,
            min=0,
            max=200,
            step=10,
            value=110,
            marks={
                0: '0',
                50: '50',
                100: '100',
                150: '150',
                200: '200',
                110: {'label': '110', 'style': {'color': 'red'}}
            }
            )]),
    html.Br(),
    dcc.Graph(id='headcount-growth'),
    html.Br(),
    html.Div(['Parking Demand: ',
        dcc.RangeSlider(
            id='parking_range',
            dots = True,
            min=0.20,
            max=0.50,
            step=0.05,
            value=[0.30, 0.45],
            allowCross = False,
            marks = {
                0.20: '25%',
                0.30: '30%',
                0.40: '40%',
                0.50: '50%'
            }
        )]),
    dcc.Graph(id='parking-demand')
])

@app.callback(
    [Output(component_id='headcount-growth', component_property='figure'),
    Output(component_id='parking-demand', component_property='figure')],
    [Input(component_id='initial-headcount', component_property='value'),
    Input(component_id='anticipated-annual-growth', component_property='value'),
    Input(component_id='parking_range', component_property='value')])

def update_headcount_growth(starting_headcount,annual_growth,parking_range):
    headcount = int(starting_headcount)
    annualGrowth = int(annual_growth)
    annualHeadcount = {}

    for y in range(0,15):
        annualHeadcount[2019 + y] = headcount
        headcount = headcount + annualGrowth

    df = pd.DataFrame(annualHeadcount.items(), columns=['Year','Headcount'])

    # Setup Headcount output
    headcount_fig = px.line(df, x="Year", y="Headcount", title="<b>Anticipated</b> Annual Headcount")

    # Begin calculations on Parking Demand
    parkingRatio_max = parking_range[1]
    parkingRadio_min = parking_range[0]
    parkingRatio = parkingRatio_max

    df['constant_demand'] = df['Headcount'] * parkingRatio

    declining_demand = []
    df['declining_demand'] = ''
    for ind in df.index:
        df['declining_demand'][ind] = df['Headcount'][ind] * parkingRatio
        parkingRatio = parkingRatio - ((parkingRatio_max-parkingRadio_min)/14)
    parking = pd.melt(df,id_vars=['Year', 'Headcount'], var_name='demand_type', value_name='demand')

    # Setup Parking Demand Output
    parking_fig = px.line(parking, x = 'Year', y = 'demand', color = 'demand_type', title = '<b>Anticipated</b> Parking Demand')

    return headcount_fig, parking_fig

if __name__ == '__main__':
    app.run_server(debug=True)
