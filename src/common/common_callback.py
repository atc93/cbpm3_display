import dash_html_components as html
import dash_core_components as dcc
import dash
from dash.dependencies import Input, Output, State


import src.tmp.layout_button_readings as button_readings
import src.tmp.layout_xymotion as xymotion
import src.online.online_layout as online
import src.offline.offline_layout as offline
import src.common.common_layout as common_layout

# though this module is under src, app is the root level module because this is the main
# script: the import is with respect to the level of the main script
from app import app
from app import conn

# @app.callback(
#     Output("online-content", "children"),
#     [Input("demo-dropdown", 'value')],
# )
# def render_menus(menu_name):
#     if menu_name == "beam_position":
#         return xymotion.build_layout()
#     elif menu_name == "button_readings":
#         return button_readings.build_layout()
    # elif menu_name == "orbit":
    #     print('building layout')
    #     return orbit.build_layout()

@app.callback(
    Output("app-content", "children"),
    [Input("real-time", "n_clicks"),
     Input("history", "n_clicks")]
)
def render_online(btn_rt, btn_his):
    if btn_rt == 0 and btn_his == 0:
        return html.Div(
            id='test',
            children=[
                html.Div(
                    common_layout.build_navbar(),
                    common_layout.build_select()
                )
            ]
        )
    elif btn_his > 0:
        return html.Div(
            id='test',
            children=[
                html.Div(offline.build_navbar()),
                html.Div(offline.build_date_picker()),
                html.Div(offline.build_analyze_button()),
                html.Div(id='date_test', children='date place holder'),
                html.Div(id='offline_content')
            ]
        )
    elif btn_rt > 0:
        return html.Div(
            children=[
                dcc.Interval(
                    id='online_auto_update',
                    interval=1 * 1000,  # in ms
                ),
                html.Div(
                    id='test',
                    children=[
                        html.Div(online.build_navbar()),
                        html.Div(id='online_content')
                    ]
                )
            ]
        )




@app.callback([Output('cbpm_xpos', 'figure'),
               Output('cbpm_ypos', 'figure'),
               Output('cbpm_xres', 'figure'),
               Output('cbpm_yres', 'figure')],
              [Input('time_window_slider', 'value'),
               Input('interval-component', 'n_intervals'),
               Input('live_update_switch', 'on')],
              [State('cbpm_xpos', 'figure'),
               State('cbpm_ypos', 'figure'),
               State('cbpm_xres', 'figure'),
               State('cbpm_yres', 'figure')])
def call_back_xymotion(time, n, switch, cbpm_xpos, cbpm_ypos, cbpm_xres, cbpm_yres):
    print(n, time, switch)
    return xymotion.update(n, time, switch, cbpm_xpos, cbpm_ypos, cbpm_xres, cbpm_yres)

@app.callback([Output('button_amp', 'figure'),
               Output('button_std', 'figure')],
              [Input('time_window_slider', 'value'),
               Input('interval-component', 'n_intervals'),
               Input('live_update_switch', 'on')],
              [State('button_amp', 'figure'),
               State('button_std', 'figure')])
def call_back_button_readings(time, n, switch, button_amp, button_std):
    # print(n, time, switch)
    return button_readings.update_plots(n, time, switch, button_amp, button_std, conn)

# ======= Callbacks for modal popup =======
@app.callback(
    Output("markdown", "style"),
    [Input("learn-more-button", "n_clicks"), Input("markdown_close", "n_clicks")],
)
def update_click_output(button_click, close_click):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "learn-more-button":
            return {"display": "block"}

    return {"display": "none"}