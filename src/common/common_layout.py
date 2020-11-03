import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def dropdown_menu():
    return html.Div(
        [
            dcc.Dropdown(
                id='demo-dropdown',
                options=[
                    {'label': 'beam position', 'value': 'beam_position'},
                    {'label': 'button readings', 'value': 'button_readings'},
                    {'label': 'orbit', 'value': 'orbit'},
                ],
                placeholder="Menu...",
            ),
        ]
    )

def build_navbar():
    return html.Div(
        children=[
            html.Div(
                className="banner",
                children=[
                    dbc.Row(
                        [
                            dbc.Col(html.Div(html.H2("CBPM display"))),
                        ],
                    ),
                ],
            ),
        ],
    )

def build_select():
    return html.Div(

        children=[

            html.Div(
                className="h1",
                children='Select the the mode:',
                style={'textAlign': 'center'}
            ),
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.Div(dbc.Button("REAL TIME", id="real-time", n_clicks=0, outline=True, color="dark", size="lg")), width="auto"),
                            dbc.Col(html.Div(html.Button("HISTORY", id="history", n_clicks=0)), width="auto"),
                        ],
                        justify="center",
                    ),
                ],
            )
        ]
    )