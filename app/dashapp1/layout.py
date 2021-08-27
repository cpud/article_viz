import dash_core_components as dcc
import dash_html_components as html
import dash_table
#import pickle
import pandas as pd
from .make_plots import make_bars, make_tables
from .cleaning import prepare_data

all_metrics = pd.DataFrame()

all_metrics, rabbit_dict, rec_percents, show_minutes, show_depth = prepare_data()
time_bars, time_scat, vid_rabbit, chan_rabbit = make_bars(all_metrics, rabbit_dict)
percent, minutes, depth, vids = make_tables(rec_percents, show_minutes, show_depth)

layout = html.Div([

    #html.Div([]),
    html.Div([
    html.Center([
    html.H3("Interactive Visualizations!"),

      
        ]),
    #html.Li('The video you submitted will have a "depth" of 1. The node will be \
     #       dark purple, so please locate that node to properly follow the graph.'),
    ], style = {'width': '98%',
                'display': 'inline-block',
                #'text-align' : 'center'
                #'padding-left': '80px',
                #'padding-top': '20px',
               }),


    # plots
    html.Div([
        #dcc.Graph(figure=fig),
        #dcc.Graph(id = 'time_bars'),
        #dcc.Graph(id = 'time_scat'),
        #dcc.Graph(id = 'vid_rabbit'),
        #dcc.Graph(id = 'chan_rabbit'),
        dcc.Graph(figure = time_bars),
        #dcc.Graph(figure = time_scat),
        dcc.Graph(figure = vid_rabbit),
        dcc.Graph(figure = percent),
        dcc.Graph(figure = depth)
    ], style = {'width': '49%',
                'display': 'inline-block'
               }
    ),

    html.Div([
        dcc.Graph(figure = time_scat),
        dcc.Graph(figure = chan_rabbit),
        dcc.Graph(figure = minutes),
        dcc.Graph(figure = vids),
        #dcc.Graph(id = 'likes'),
        #dcc.Graph(figure = fig4),
        #dcc.Graph(id = 'views'),
        #dcc.Graph(figure = fig6)
        #dcc.Graph(id = 'comments'),
    ], style = {'width': '49%',
                'display': 'inline-block'
               }
    ),

    #html.Div(id = 'table',
    #         style = {'width': '98%',
    #            #'display': 'inline-block'
    #            }
    #),



], #style = {'columnCount': '2'}
)
