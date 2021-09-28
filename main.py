import numpy as np
import pandas as pd
import copy
import argparse


from logLoader import loadLogFileToDF
from dataPreparation import dataPreparation
from dataExtraction import (
    getStatusCodeCount,
    getStatusCodeTimeLine,
    getUsageHours,
    getRequestCount,
    getUsageDays,
    getReferrer,
    getOverallStats,
)
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import plotly.io as pio
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import date, datetime
from dash.exceptions import PreventUpdate


app = dash.Dash("Apache SSL Log Analyzer & Dashboard",
                external_stylesheets=[dbc.themes.DARKLY])


pio.templates.default = "plotly_dark"


def main(path):
    try:
        df = loadLogFileToDF(path)

        df = dataPreparation(df)
        ref, rc, scc, tscc, uh, ud, allg = getData(df)

        fig, fig2, fig3, fig4, fig5, fig6, lists = getFigs(
        ref, rc, scc, tscc, uh, ud, allg)

        app.layout = html.Div(
        [

            dbc.Row([
                dbc.Col(html.H1(children="Apache SSL Log Analyzer & Dashboard"), style={
                        'padding-top': '25px', 'padding-left': '50px'}),
                dbc.Col([dcc.DatePickerRange(
                    id='date-picker-range',
                    display_format='DD.MM.YYYY',
                    start_date_placeholder_text='DD.MM.YYYY',
                    end_date_placeholder_text='DD.MM.YYYY'
                ), html.P("*Updating takes some time")
                ], style={'text-align': 'right', 'background': 'rgb(17, 17, 17)', 'padding-top': '25px', 'padding-right': '50px'}),
            ]),

            html.Hr(style={'border-color': 'white'}),

            dcc.Loading(
                id="loading-1",
                type="cube",
                children=[
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H5('Overall Stats:', style={
                                'padding-top': '25px', 'padding-left': '50px'}),
                            html.Div([lists], id="overall-stats",),
                        ]),),
                        dbc.Col(html.Div([
                            html.H5('Daily Calls:', style={
                                'padding-top': '25px', 'padding-left': '50px'}),
                            dcc.Graph(id="ud", figure=fig5),

                        ]),),
                    ]),
                    html.H5('Avg. Usages by quarter hours:', style={
                        'padding-top': '25px', 'padding-left': '50px'}),
                    dcc.Graph(id="ug", figure=fig3),
                    html.Hr(style={'border-color': 'white'}),


                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H5('Status Code Time Line:', style={
                                'padding-top': '25px', 'padding-left': '50px'}),
                            dcc.Graph(id="time-series", figure=fig2),
                        ]),),
                        dbc.Col(html.Div([
                            html.H5('Status Code Distribution:', style={
                                'padding-top': '25px', 'padding-left': '50px'}),
                            dcc.Graph(id="pie-chart", figure=fig),
                        ]),),
                    ]),
                    html.Hr(style={'border-color': 'white'}),


                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H5('Most used API Routes:', style={
                                'padding-top': '25px', 'padding-left': '50px'}),
                            dcc.Graph(id="rc", figure=fig4),
                        ]),),
                        dbc.Col(html.Div([
                            html.H5('Top 5 Referer:', style={
                                'padding-top': '25px', 'padding-left': '50px'}),
                            dcc.Graph(id="ref", figure=fig6),
                        ]),),
                    ]),
                    html.Hr(style={'border-color': 'white'}),
                    html.Div(["Developed by ", html.A(children=["Niklas Ullmann"], href="https://niklas-ullmann.de/", target="_blank")],
                             style={'padding-left': '50px', })
                ]
            ),
        ],
        style={'background': 'rgb(17, 17, 17)'}
    )

        @app.callback(
        [dash.dependencies.Output('pie-chart', 'figure'),
         dash.dependencies.Output('time-series', 'figure'),
         dash.dependencies.Output('ug', 'figure'),
         dash.dependencies.Output('rc', 'figure'),
         dash.dependencies.Output('ud', 'figure'),
         dash.dependencies.Output('ref', 'figure'),
         dash.dependencies.Output('overall-stats', 'children'), ],
        [dash.dependencies.Input('date-picker-range', 'start_date'),
         dash.dependencies.Input('date-picker-range', 'end_date')],
    )
        def update_output(start_date, end_date):
            if start_date is not None and end_date is not None:
                x = copy.deepcopy(df)
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d')

                x['Datetime'] = pd.to_datetime(x[['year', 'month', 'day']].astype(
                str).apply(' '.join, 1), format='%Y %m %d')
                y = x[x['Datetime'].between(start, end)]

                if(y.shape[0] <= 0):
                    print("No Logs for this time period")
                    raise PreventUpdate

                ref, rc, scc, tscc, uh, ud, allg = getData(y)

                fig, fig2, fig3, fig4, fig5, fig6, lists = getFigs(
                ref, rc, scc, tscc, uh, ud, allg)

                return fig, fig2, fig3, fig4, fig5, fig6, lists

            else:
                raise PreventUpdate
    
    except Exception as err:
        print("Failed to analyze log file:")
        print(err)

    app.run_server(debug=False)


def getData(df):

    ref = getReferrer(copy.deepcopy(df))
    rc = getRequestCount(copy.deepcopy(df))
    scc = getStatusCodeCount(copy.deepcopy(df))
    tscc = getStatusCodeTimeLine(copy.deepcopy(df))
    uh = getUsageHours(copy.deepcopy(df))
    ud = getUsageDays(copy.deepcopy(df))
    allg = getOverallStats(copy.deepcopy(df))

    return ref, rc, scc, tscc, uh, ud, allg


def getFigs(ref, rc, scc, tscc, uh, ud, allg):

    fig = px.pie(scc, values="count", names="status")
    fig2 = px.line(tscc, x="date", y=tscc.columns)
    fig3 = go.Figure(data=[
        go.Bar(
            x=uh['time'],
            y=uh['counts']
        ),
        go.Scatter(
            x=uh['time'],
            y=uh['bestfit']
        )

    ])
    fig3.update_layout(showlegend=False)
    fig4 = px.bar(rc, x="counts", y="request", orientation="h")
    fig5 = go.Figure(data=[
        go.Scatter(
            x=ud['date'],
            y=ud['counts']
        ),
        go.Scatter(
            x=ud['date'],
            y=ud['bestfit']
        )

    ])
    fig5.update_layout(showlegend=False)
    #fig5 = px.line(ud, x="date", y="counts")
    fig6 = px.pie(ref, values="counts", names="referrer")

    lists = createOverallList(allg)

    return fig, fig2, fig3, fig4, fig5, fig6, lists


def createOverallList(allg):

    return html.Ul(
        children=[html.H3(html.Li('Amount of Logs: {}'.format(allg["length"])),  style={'padding-left': '50px', }),
                  html.H3(html.Li('Starting from: {}'.format(
                      allg["start"])),  style={'padding-left': '50px', }),
                  html.H3(html.Li('Ending with: {}'.format(allg["end"])),  style={
                          'padding-left': '50px', }),
                  html.H3(html.Li('Evaluating Logs off: {} Days'.format(
                      allg["delta"])),  style={'padding-left': '50px', }),

                  ],  style={'padding-left': '50px', }
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Path to LogFile')
    parser.add_argument("--path", type=str, default="access_ssl_log")
    args = parser.parse_args()
    path = args.path
    main(path)
