# -*- coding: utf-8 -*-

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

import src.utils.database as db
import src.common.common_layout as common_layout

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__)#, external_stylesheets=external_stylesheets)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder="./assets")
app.config.suppress_callback_exceptions = True

server = app.server

conn = db.initialize()


def server_layout():
    return html.Div(
        id="app-content",
        children=[
            common_layout.build_navbar(),
            common_layout.build_select()
        ]
    )


app.layout = server_layout

from src.online import online_callback
from src.offline import offline_callback
from src.common import common_callback

if __name__ == '__main__':
    # with PyCallGraph(output=GraphvizOutput()):
    app.run_server(host='127.0.0.1', port='8000', debug=True)
