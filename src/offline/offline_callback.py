from app import app, conn

from dash.dependencies import Input, Output, State

import pandas as pd

import src.utils.database as db
import src.utils.process_data as analyze
import src.offline.offline_orbit as orbit


# df: DataFrame = pd.DataFrame()

@app.callback(Output("offline_store_df", "children"),
              [Input("button_analyze", 'n_clicks')],
              [State("date_picker", "start_date"),
               State("date_picker", "end_date"),
               State("time_select_min", "value"),
               State("time_select_max", "value")]
)
def offline_callback(click, start_date, end_date, time_select_min, time_select_max):
    print(click, start_date, end_date, time_select_min, time_select_max)
    if click > 0:
        df = db.get_offline_data_from_db(conn, start_date, end_date, time_select_min, time_select_max)
        df = analyze.position(df)
        # df = analyze.detloc_detid_mapping(df)
        # df = df[:10]
        # return orbit.update(df, True)
        # return df.to_json(date_format='iso', orient='split')
        df = analyze.decimate(df)
        return df.to_json(date_format='epoch', orient='split')



@app.callback([Output("offline_content", "children"),
               Output('orbit_x', 'figure'),
               Output('orbit_y', 'figure')],
              [Input("demo-dropdown", 'value'),
              Input('offline_store_df', 'children')]
              )
def callback_orbit(menu, df):
    df = pd.read_json(df, orient='split')
    if menu == 'orbit':
        # print(df.head())
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        orbit_x, orbit_y = orbit.update(df, True)
        return orbit.build_layout(), orbit_x, orbit_y
    # elif menu == "beam_position":
    #     return xymotion.build_layout()
    # elif menu == "button_readings":
    #     return button_readings.build_layout()

# https://dash.plotly.com/sharing-data-between-callbacks