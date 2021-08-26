import pandas as pd

def prepare_data():
    comm_full_stacked = pd.read_csv('data/comm_full_stacked.csv')
    comm_selected_stacked = pd.read_csv('data/comm_selected_stacked.csv')
    pr_full_stacked = pd.read_csv('data/pr_full_stacked.csv')
    pr_selected_stacked = pd.read_csv('data/pr_selected_stacked.csv')
    tr_full_stacked = pd.read_csv('data/tr_full_stacked.csv')
    tr_selected_stacked = pd.read_csv('data/tr_selected_stacked.csv')
    office_full_stacked = pd.read_csv('data/office_full_stacked.csv')
    office_selected_stacked = pd.read_csv('data/office_selected_stacked.csv')
    all_metrics = pd.read_csv('data/all_metrics.csv')

    # make dictionaries to make rabbit hole charts
    rabbit_dict = {}
    rabbit_dict['tr_channels'] = tr_selected_stacked[tr_selected_stacked['Channel'] != '30 Rock Official']['Channel'].value_counts()
    rabbit_dict['tr_vids'] = tr_selected_stacked[tr_selected_stacked['Channel'] != '30 Rock Official']['Title'].value_counts()
    rabbit_dict['pr_channels'] = pr_selected_stacked[pr_selected_stacked['Channel'] != 'Parks and Recreation']['Channel'].value_counts()
    rabbit_dict['pr_vids'] = pr_selected_stacked[pr_selected_stacked['Channel'] != 'Parks and Recreation']['Title'].value_counts()
    rabbit_dict['office_channels'] = office_selected_stacked[office_selected_stacked['Channel'] != 'The Office']['Channel'].value_counts()
    rabbit_dict['office_vids'] = office_selected_stacked[office_selected_stacked['Channel'] != 'The Office']['Title'].value_counts()
    rabbit_dict['comm_channels'] = comm_selected_stacked[comm_selected_stacked['Channel'] != 'Community']['Channel'].value_counts()
    rabbit_dict['comm_vids'] = comm_selected_stacked[comm_selected_stacked['Channel'] != 'Community']['Title'].value_counts()

    # list for percent table
    rec_percents = []
    tr_percent = round(len(tr_full_stacked[tr_full_stacked['Channel'] == '30 Rock Official']) / sum(tr_full_stacked['Channel'].value_counts()),3) * 100
    pr_percent = round(len(pr_full_stacked[pr_full_stacked['Channel'] == 'Parks and Recreation']) / sum(pr_full_stacked['Channel'].value_counts()),3) * 100
    comm_percent = round(len(comm_full_stacked[comm_full_stacked['Channel'] == 'Community']) / sum(comm_full_stacked['Channel'].value_counts()),3) * 100
    office_percent = round(len(office_full_stacked[office_full_stacked['Channel'] == 'The Office']) / sum(office_full_stacked['Channel'].value_counts()),3) * 100

    rec_percents.append(str(tr_percent))
    rec_percents.append(str(pr_percent))
    rec_percents.append(str(comm_percent))
    rec_percents.append(str(office_percent)[:4])

    # list for minutes table
    show_minutes = []
    tr_min = round(tr_selected_stacked[tr_selected_stacked['Channel'] == '30 Rock Official']['Minutes'].mean(),3)
    pr_min = round(pr_selected_stacked[pr_selected_stacked['Channel'] == 'Parks and Recreation']['Minutes'].mean(),3)
    comm_min = round(comm_selected_stacked[comm_selected_stacked['Channel'] == 'Community']['Minutes'].mean(),3)
    office_min = round(office_selected_stacked[office_selected_stacked['Channel'] == 'The Office']['Minutes'].mean(),3)
    show_minutes.append(tr_min)
    show_minutes.append(pr_min)
    show_minutes.append(comm_min)
    show_minutes.append(office_min)

    # list for depth table
    show_depth = []
    tr_depth = round(tr_selected_stacked['Depth'].mean(),3)
    pr_depth = round(pr_selected_stacked['Depth'].mean(),3)
    comm_depth = round(comm_selected_stacked['Depth'].mean(),3)
    office_depth = round(office_selected_stacked['Depth'].mean(),3)
    show_depth.append(tr_depth)
    show_depth.append(pr_depth)
    show_depth.append(comm_depth)
    show_depth.append(office_depth)

    return all_metrics, rabbit_dict, rec_percents, show_minutes, show_depth
