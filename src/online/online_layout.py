import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import dash_bootstrap_components as dbc

import src.common.common_layout as layout_common


def build_navbar():
    return html.Div(
        id="banner",
        children=[
            html.Div(
                id="banner-text",
                className="banner",
                children=[
                    dbc.Row(
                        [
                            dbc.Col(html.Div(html.H2("CBPM real-time display")), width=11),
                            dbc.Col(
                                html.Div(
                                    id="banner-logo",
                                    children=[
                                        html.Button(
                                            id="learn-more-button", children="INFORMATION", n_clicks=0
                                        ),
                                    ],
                                ),
                            )
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
                                html.Div(
                                    daq.PowerButton(
                                        id='live_update_switch',
                                        on='True',
                                        size=50,
                                        color='#079407',
                                        # label='Label',
                                        # labelPosition='top'
                                    ),
                                    id='test_button',
                                    style={'padding': '10px 0px 0px 0px'},
                                ), width={"size": 1},
                            ),
                            dbc.Col(
                                html.Div(
                                    children=[
                                        html.H2("Live update is:"),
                                        html.H2(
                                            id='live_update_running',
                                            style={'margin-left': '1.0%', 'color': '#079407', 'font-weight': 'bold'},
                                        ),
                                        html.H2(
                                            id='live_update_paused',
                                            style={'margin-left': '0.5%', 'color': '#e0392a', 'font-weight': 'bold'},
                                        ),
                                    ],
                                ), #style={'padding': '0px 1000px 0px 0px'},
                            ),
                            dbc.Col(
                                html.Div(id='offline_store_df', style={'display': 'none'}),
                            ),
                            dbc.Col(
                                layout_common.dropdown_menu(), width=2,
                            )
                        ], no_gutters=True, justify='start',
                    )
                ]
            )
        ],
    )

def generate_modal():
    return html.Div(
        id="markdown",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=dcc.Markdown(
                            children=(
                                """
                        ###### What is this mock app about?
                        This is a dashboard for monitoring real-time process quality along manufacture production line.
                        ###### What does this app shows
                        Click on buttons in `Parameter` column to visualize details of measurement trendlines on the bottom panel.
                        The sparkline on top panel and control chart on bottom panel show Shewhart process monitor using mock data.
                        The trend is updated every other second to simulate real-time measurements. Data falling outside of six-sigma control limit are signals indicating 'Out of Control(OOC)', and will
                        trigger alerts instantly for a detailed checkup.

                        Operators may stop measurement by clicking on `Stop` button, and edit specification parameters by clicking specification tab.
                    """
                            )
                        ),
                    ),
                ],
            )
        ),
    )