import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from datetime import datetime as dt
from datetime import timedelta

import src.common.common_layout as layout_common

def build_navbar():
    return html.Div(
        children=[
            html.Div(
                className="banner",
                children=[
                    dbc.Row(
                        [
                            dbc.Col(html.Div(html.H2("CBPM display -- history mode"))),
                        ],
                    ),
                ],
            ),
            html.Div(
                className="banner2",
                children=[
                    dbc.Row(
                        [
                            dbc.Col(

                                layout_common.dropdown_menu(), width=2,
                            )
                        ], no_gutters=True, justify='end',
                    )
                ]
            )
        ],
    )

def build_date_picker():
    return html.Div([
        dcc.DatePickerRange(
            id='date_picker',
            # min_date_allowed=dt(2020, 7, 14),
            # max_date_allowed=dt(2020, 7, 15),
            initial_visible_month=dt(dt.today().year, dt.today().month, dt.today().day),
            start_date=(dt(dt.today().year, dt.today().month, dt.today().day)-timedelta(days=15)).date(),
            end_date=dt(dt.today().year, dt.today().month, dt.today().day).date(),
            calendar_orientation='vertical',
        ),
        # Hidden div inside the app that stores the intermediate value
        html.Div(id='offline_store_df', style={'display': 'none'}),
        html.Div(id='analyzed-data'),
        html.Div(id='output-container-date-picker-range'),
        dcc.Input(
            id='time_select_min',
            type='time',
            placeholder='input type',
            value='08:40'
        ),
        dcc.Input(
            id='time_select_max',
            type='time',
            placeholder='input type',
            value='08:50'
        )
    ])


def build_analyze_button():
    return html.Div(
        className="h1",
        children=[
            dbc.Row(
                [
                    dbc.Col(dbc.Button("ANALYZE", id="button_analyze", n_clicks=0, outline=True, color="dark", size="lg"), width="auto"),
                ],
                justify="center",
            ),
        ],
    )