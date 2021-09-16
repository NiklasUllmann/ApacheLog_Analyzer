import numpy as np
import pandas as pd
import copy

from logLoader import loadLogFileToDF
from dataPreparation import dataPreparation
from dataExtraction import (
    getStatusCodeCount,
    getStatusCodeTimeLine,
    getUsageHours,
    getRequestCount,
    getUsageDays,
    getReferrer,
)
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import plotly.io as pio
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import date


app = dash.Dash("Apache SSL Log Analyzer & Dashboard",
                external_stylesheets=[dbc.themes.DARKLY])


pio.templates.default = "plotly_dark"


def main():
    df = loadLogFileToDF("../data/access_ssl_log")

    df = dataPreparation(df)

    ref = getReferrer(copy.deepcopy(df))

    rc = getRequestCount(copy.deepcopy(df))
    scc = getStatusCodeCount(copy.deepcopy(df))
    tscc = getStatusCodeTimeLine(copy.deepcopy(df))
    uh = getUsageHours(copy.deepcopy(df))
    ud = getUsageDays(copy.deepcopy(df))

    fig = px.pie(scc, values="count", names="status")

    fig2 = px.line(tscc, x="date", y=tscc.columns)

    data = [
        go.Bar(
            x=uh['time'],
            y=uh['counts']
        ),
        go.Scatter(
            x=uh['time'],
            y=uh['bestfit']
        )

    ]

    fig3 = go.Figure(data=data)
    fig3.update_layout(showlegend=False)

    fig4 = px.bar(rc, x="counts", y="request", orientation="h")

    fig5 = px.line(ud, x="date", y="counts")

    fig6 = px.pie(ref, values="counts", names="referrer")

    app.layout = html.Div(
        [

            dbc.Row([
                dbc.Col(html.H1(children="Apache SSL Log Analyzer & Dashboard"),),
                dbc.Col(dcc.DatePickerRange(
                    end_date=date(2017, 6, 21),
                    display_format='MMM Do, YY',
                    start_date_placeholder_text='MMM Do, YY'
                ),),
            ]),

            html.Hr(style={'border-color': 'white'}),


            dbc.Row([
                dbc.Col(html.Div([
                    html.H5('Overall Stats:'),
                ]),),
                dbc.Col(html.Div([
                    html.H5('Daily Calls:'),
                    dcc.Graph(id="ud", figure=fig5),

                ]),),
            ]),
            html.H5('Usages by quarter hours:'),
            dcc.Graph(id="ug", figure=fig3),
            html.Hr(style={'border-color': 'white'}),


            dbc.Row([
                dbc.Col(html.Div([
                    html.H5('Status Code Time Line:'),
                    dcc.Graph(id="time-series", figure=fig2),
                ]),),
                dbc.Col(html.Div([
                    html.H5('Status Code Distribution:'),
                    dcc.Graph(id="pie-chart", figure=fig),
                ]),),
            ]),
            html.Hr(style={'border-color': 'white'}),


            dbc.Row([
                dbc.Col(html.Div([
                    html.H5('Most used API Routes:'),
                    dcc.Graph(id="rc", figure=fig4),
                ]),),
                dbc.Col(html.Div([
                    html.H5('Top 5 Referer:'),
                    dcc.Graph(id="ref", figure=fig6),
                ]),),
            ]),
            html.Hr(style={'border-color': 'white'}),
        ],
        style={'background': 'rgb(17, 17, 17)'}
    )

    app.run_server(debug=False)


if __name__ == "__main__":
    main()
