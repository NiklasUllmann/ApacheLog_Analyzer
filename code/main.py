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

import logging


app = dash.Dash("Apache SSL Log Analyzer & Dashboard")

logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
)
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler("{0}/{1}.log".format("./logs", "logfile"))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
rootLogger.setLevel(logging.DEBUG)


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

    fig3 = px.bar(uh, x="time", y="counts")

    fig4 = px.bar(rc, x="counts", y="request", orientation="h")

    fig5 = px.line(ud, x="date", y="counts")

    app.layout = html.Div(
        [
            html.H1(children="HTTP Status Codes"),
            dcc.Graph(id="pie-chart", figure=fig),
            dcc.Graph(id="time-series", figure=fig2),
            dcc.Graph(id="ug", figure=fig3),
            dcc.Graph(id="rc", figure=fig4),
            dcc.Graph(id="uh", figure=fig5),
        ]
    )

    app.run_server(debug=False)


if __name__ == "__main__":
    main()