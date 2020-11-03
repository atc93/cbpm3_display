from app import app, conn

# import sys
# sys.path.append("..")
from dash.dependencies import Input, Output

import src.utils.database as db
import src.utils.process_data as analyze
import src.online.online_orbit as orbit

@app.callback(
    [Output(component_id='live_update_running', component_property='children'),
     Output(component_id='live_update_paused', component_property='children')],
    [Input('live_update_switch', 'on')]
)
def change_live_text_status(switch):
    if switch:
        return ("RUNNING", "")
    elif not switch:
        return ("", "PAUSED")


@app.callback([Output("online_content", "children"),
              Output('online_orbit_hor', 'figure'),
              Output('online_orbit_ver', 'figure')],
              [Input("demo-dropdown", 'value'),
               Input('online_auto_update', 'n_intervals'),
               Input('live_update_switch', 'on')]
)
def callback_online_orbit(menu_name, n_int, switch):
    print(menu_name, n_int, switch)
    if menu_name == 'orbit':
        df = db.get_online_data_from_db(conn)
        df = analyze.position(df)
        df = analyze.detloc_detid_mapping(df)
        orbit_x, orbit_y = orbit.update(df, switch)
        return orbit.build_layout(), orbit_x, orbit_y

