# -*- coding: utf-8 -*-

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as table
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px


def build_layout():
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            dcc.Graph(id='orbit_x')
                        ),
                        width=6
                    ),
                    dbc.Col(
                        html.Div(
                            children=[
                                dcc.Graph(id='orbit_y'),

                            ]
                        ),
                        width=6
                    ),
                ], style={'margin-top': '-25px'}
            )
        ]
    )


def update(df, switch):
    if switch:

        print('hello')

        fig = []
        fig.append(plotly.subplots.make_subplots())
        fig.append(plotly.subplots.make_subplots())


        yaxis_label = ['Horizontal position [micron]',
                       'Vertical position [micron]']

        yaxis_data = ['xpos',
                      'ypos',]

        print(df.head(10))
        fig[0] = px.scatter(df, x="instr", y="xpos", animation_frame="timestamp")
        fig[0]["layout"].pop("updatemenus")  # optional, drop animation buttons

        fig[1] = px.scatter(df, x="instr", y="ypos", animation_frame="timestamp")
        fig[1]["layout"].pop("updatemenus")  # optional, drop animation buttons

        # for i in range(len(fig)):
        #
        #     fig[i].update_layout(
        #         height=500,
        #         template='plotly_white'
        #     )
        #
        #     # fig[i]['layout']['xaxis'].update(title='Time [hh:mm:ss]', title_font=dict(size=25), tickfont=dict(size=18))
        #     # fig[i]['layout']['xaxis'].update(gridcolor='grey', showline=True, linewidth=2, linecolor='grey', mirror=True)
        #     fig[i].update_xaxes(
        #         title='Time [hh:mm:ss]',
        #         title_font=dict(size=20),
        #         tickfont=dict(size=18),
        #         gridcolor='grey',
        #         showline=True,
        #         linewidth=2,
        #         linecolor='grey',
        #         mirror=True
        #     )
        #
        #     fig[i].update_yaxes(
        #         title=yaxis_label[i],
        #         title_font=dict(size=20),
        #         tickfont=dict(size=18),
        #         gridcolor='grey',
        #         showline=True,
        #         linewidth=2,
        #         linecolor='grey',
        #         mirror=True,
        #         zeroline=True,
        #         zerolinecolor='grey',
        #         zerolinewidth=1,
        #         # automargin=True
        #     )
        #
        #     # fig[i]['layout']['plot_bgcolor'] = 'rgb(0, 0, 0, 0)'
        #     # fig[i]['layout']['paper_bgcolor'] = 'rgb(0, 0, 0, 333)'
        #
        #     fig[i].add_trace(
        #         go.Scatter(
        #             x=df.index,
        #             y=df[yaxis_data[i]],
        #             name="position"
        #         ),
        #         secondary_y=False
        #     )

        return fig[0], fig[1]
        # return [f for f in fig]

def update_online(df, switch):
    if switch:

        print('hello')

        fig = []
        fig.append(plotly.subplots.make_subplots())
        fig.append(plotly.subplots.make_subplots())


        yaxis_label = ['Horizontal position [micron]',
                       'Vertical position [micron]']

        yaxis_data = ['xpos',
                      'ypos',]

        for i in range(len(fig)):

            fig[i].update_layout(
                height=500,
                template='plotly_white'
            )

            # fig[i]['layout']['xaxis'].update(title='Time [hh:mm:ss]', title_font=dict(size=25), tickfont=dict(size=18))
            # fig[i]['layout']['xaxis'].update(gridcolor='grey', showline=True, linewidth=2, linecolor='grey', mirror=True)
            fig[i].update_xaxes(
                title='Time [hh:mm:ss]',
                title_font=dict(size=20),
                tickfont=dict(size=18),
                gridcolor='grey',
                showline=True,
                linewidth=2,
                linecolor='grey',
                mirror=True
            )

            fig[i].update_yaxes(
                title=yaxis_label[i],
                title_font=dict(size=20),
                tickfont=dict(size=18),
                gridcolor='grey',
                showline=True,
                linewidth=2,
                linecolor='grey',
                mirror=True,
                zeroline=True,
                zerolinecolor='grey',
                zerolinewidth=1,
                # automargin=True
            )

            # fig[i]['layout']['plot_bgcolor'] = 'rgb(0, 0, 0, 0)'
            # fig[i]['layout']['paper_bgcolor'] = 'rgb(0, 0, 0, 333)'

            fig[i].add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[yaxis_data[i]],
                    name="position"
                ),
                secondary_y=False
            )

        return [f for f in fig]