import numpy as np
import pandas as pd
import plotly.graph_objects as go
from textblob import TextBlob
from datetime import datetime

def make_bars(all_metrics, rabbit_dict):
    """Take all_metrics df and make bar charts"""
    # time spent on channel bars
    time_bars = go.Figure(data = [
        go.Bar(
            name = 'Duration Mean',
            x = all_metrics['Show'].unique().tolist(),
            y = all_metrics.groupby(by = ['Show']).mean()['Duration']),
        go.Bar(
            name = 'Duration Std',
            x = all_metrics['Show'].unique().tolist(),
            y = all_metrics.groupby(by = ['Show']).std()['Duration']),
        ])
    time_bars.update_layout(colorway = ['#3e4989', '#1f9e89'],
                      yaxis_title = 'Duration (Minutes)',
                      xaxis_title = 'Show',
                      title = 'Time Spent On Channel')

    # time spent on channel scatter
    time_scat = go.Figure()
    time_scat.add_trace(go.Scatter(x = all_metrics[all_metrics['Show'] == 'The Office']['Run'],
                             y = all_metrics[all_metrics['Show'] == 'The Office']['Duration'],
                             mode = 'lines',
                             name = 'The Office'))
    time_scat.add_trace(go.Scatter(x = all_metrics[all_metrics['Show'] == 'Community']['Run'],
                             y = all_metrics[all_metrics['Show'] == 'Community']['Duration'],
                             mode = 'lines',
                             name = 'Community'))
    time_scat.add_trace(go.Scatter(x = all_metrics[all_metrics['Show'] == 'Parks and Recreation']['Run'],
                             y = all_metrics[all_metrics['Show'] == 'Parks and Recreation']['Duration'],
                             mode = 'lines',
                             name = 'Parks and Recreation'))
    time_scat.add_trace(go.Scatter(x = all_metrics[all_metrics['Show'] == '30 Rock Official']['Run'],
                             y = all_metrics[all_metrics['Show'] == '30 Rock Official']['Duration'],
                             mode = 'lines',
                             name = '30 Rock'))

    time_scat.update_layout(title = 'Time Spent On Channel',
                      xaxis_title = 'Run',
                      yaxis_title = 'Duration (Minutes)')

    # videos that ended rabbit holes
    vid_rabbit = go.Figure()
    vid_rabbit.add_trace(go.Bar(
        name = 'Community',
        x = rabbit_dict['comm_vids'].index[:3],
        y = rabbit_dict['comm_vids'][:3]))
    vid_rabbit.add_trace(go.Bar(
        name = 'Parks & Rec',
        x = rabbit_dict['pr_vids'].index[:3],
        y = rabbit_dict['pr_vids'][:3]))
    vid_rabbit.add_trace(go.Bar(
        name = '30 Rock',
        x = rabbit_dict['tr_vids'].index[:3],
        y = rabbit_dict['tr_vids'][:3]))
    vid_rabbit.add_trace(go.Bar(
        name = 'The Office',
        x = rabbit_dict['office_vids'].index[:3],
        y = rabbit_dict['office_vids'][:3]))
    #colorway = ['#3e4989', '#1f9e89']
    vid_rabbit.update_layout(colorway=["magenta", "green", "blue", "goldenrod"],
                      title = 'Videos That Ended Rabbit Holes Most Often',
                      xaxis_title = 'Video Title',
                      yaxis_title = 'Count'
                    #colorscale = 'viridis'
        )
        # videos that ended rabbit holes
    chan_rabbit = go.Figure()
    chan_rabbit.add_trace(go.Bar(
        name = 'Community',
        x = rabbit_dict['comm_channels'].index[:3],
        y = rabbit_dict['comm_channels'][:3]))
    chan_rabbit.add_trace(go.Bar(
        name = 'Parks & Rec',
        x = rabbit_dict['pr_channels'].index[:3],
        y = rabbit_dict['pr_channels'][:3]))
    chan_rabbit.add_trace(go.Bar(
        name = '30 Rock',
        x = rabbit_dict['tr_channels'].index[:3],
        y = rabbit_dict['tr_channels'][:3]))
    chan_rabbit.add_trace(go.Bar(
        name = 'The Office',
        x = rabbit_dict['office_channels'].index[:3],
        y = rabbit_dict['office_channels'][:3]))
        #colorway = ['#3e4989', '#1f9e89']
    chan_rabbit.update_layout(colorway=["magenta", "green", "blue", "goldenrod"],
                          title = 'Channels That Ended Rabbit Holes Most Often',
                          xaxis_title = 'Channel Name',
                          yaxis_title = 'Count'
                        #colorscale = 'viridis'
                        )
    return time_bars, time_scat, vid_rabbit, chan_rabbit

def make_tables(rec_percents, show_minutes, show_depth):
    percent = go.Figure(data=[go.Table(
        header=dict(values=['Show', 'Percentage'],
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='center'),
        cells=dict(values=[['30 Rock', 'Parks & Recreation', 'Community', 'The Office'], # 1st column
                           rec_percents], # 2nd column
                   line_color='darkslategray',
                   fill_color='lightcyan',
                   align='center'))
    ])

    minutes = go.Figure(data=[go.Table(
        header=dict(values=['Show', 'Minutes'],
                    line_color='darkslategray',
                    fill_color='coral',
                    align='center'),
        cells=dict(values=[['30 Rock', 'Parks & Recreation', 'Community', 'The Office'], # 1st column
                           show_minutes], # 2nd column
                   line_color='darkslategray',
                   fill_color='orange',
                   align='center'))
    ])

    depth = go.Figure(data=[go.Table(
        header=dict(values=['Show', 'Average Depth'],
                    line_color='darkslategray',
                    fill_color='gray',
                    align='center'),
        cells=dict(values=[['30 Rock', 'Parks & Recreation', 'Community', 'The Office'], # 1st column
                           show_depth], # 2nd column
                   line_color='darkslategray',
                   fill_color='lightgreen',
                   align='center'))
    ])

    vids = go.Figure(data=[go.Table(
        header=dict(values=['Show', 'Videos'],
                    line_color='darkslategray',
                    fill_color='gray',
                    align='center'),
        cells=dict(values=[['30 Rock', 'Parks & Recreation', 'Community', 'The Office'], # 1st column
                           [499, 674, 291, 718]], # 2nd column
                   line_color='darkslategray',
                   fill_color='pink',
                   align='center'))
    ])


    return percent, minutes, depth, vids
