
import numpy as np
import pandas as pd
import copy

from logLoader import loadLogFileToDF
from dataPreparation import dataPreparation
from dataExtraction import getStatusCodeCount, getStatusCodeTimeLine, getUsageHours
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash("Apache SSL Log Analyzer & Dashboard")

def main():
    df = loadLogFileToDF("../data/access_ssl_log")

    df = dataPreparation(df)

    


    scc = getStatusCodeCount(copy.deepcopy(df))
    tscc = getStatusCodeTimeLine(copy.deepcopy(df))
    uh = getUsageHours(copy.deepcopy(df))

    fig = px.pie(scc, values="count", names="status")

    fig2 = px.line(tscc, x="date", y=tscc.columns)

    fig3 = px.bar(uh, x="time", y="counts")


    app.layout = html.Div([
        html.H1(children='HTTP Status Codes'),
    
    dcc.Graph(id="pie-chart", figure=fig),
    dcc.Graph(id="time-series", figure=fig2),
    dcc.Graph(id="ug", figure= fig3),
])




    app.run_server(debug=False)


if __name__ == "__main__":
    main()