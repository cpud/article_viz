import json
import pandas as pd
import os
import time
from googleapiclient.discovery import build
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
#import networkx as nx
import random
from igraph import Graph
import plotly.graph_objects as go
from textblob import TextBlob

def get_related_data(driver):
    """This will use the webdriver to grab the titles and links
    to both the selected video and the first 10 recommended videos."""
    #driver = webdriver.Chrome(executable_path = 'chromedriver_linux64/chromedriver')
    #driver.get(url)

    # possibly excessive amount of time to wait for data to load
    time.sleep(2)

    # selected video title
    selected_title_path = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string')
    selected_title = selected_title_path.text

    # get titles - unnecessary due to API calls but does work consistently
    related_videos = driver.find_elements_by_xpath("//*[@id='video-title']")
    related_video_titles = [videos.text for videos in related_videos]
    related_video_titles = related_video_titles[:10]
    # add selected title to top of list
    related_video_titles.insert(0, selected_title)

    # get links
    related_links = driver.find_elements_by_xpath("//*[@id='dismissible']/div/div[1]/a")
    related_links_out = [link.get_attribute('href') for link in related_links]
    related_links_out = related_links_out[:10]
    # add selected link to top of list
    related_links_out.insert(0, url)

    # we need to remove playlists from suggestions, as they require a different API call.
    # dictionary to zip links/titles together for filtering.
    data_dict = dict(zip(related_links_out, related_video_titles))
    # store filtered values.
    filt_dict = {}

    # removing links with substring 'list' will avoid all suggested playlists/mixes.
    for link in data_dict.keys():
        if 'list' not in link:
            filt_dict.update({link:data_dict[link]})


    # store in dataframe
    out_df = pd.DataFrame()
    out_df['Title'] = filt_dict.values()
    out_df['Link'] = filt_dict.keys()

    # parse for URI for API use
    out_df['Id'] = out_df['Link'].apply(lambda x: x.split('=')[1])

    return out_df

def related_api_requests(in_df):
    """This function makes calls to the youtube API to get information on
    the submitted videos"""
    # update func/variable names
    # limit to 50 at a time??
    # build youtube resource object
    youtube = build('youtube','v3',developerKey='AIzaSyCgwz5GP-y0t2u1srVZvaolyZkfARwKNwM')

    # video Ids to feed into API
    related_Ids = list(in_df['Id'])

    # contentDetails videos request to get video length
    vid_request = youtube.videos().list(
        part = 'contentDetails',
        id = related_Ids)
    vid_response = vid_request.execute()

    # loop through durations
    durations = []
    for item in vid_response['items']:
        durations.append(item['contentDetails']['duration'])

    # stat request for likes, dislikes, comment counts, and view counts
    stat_request = youtube.videos().list(
        part = 'statistics',
        id = related_Ids)
    stat_response = stat_request.execute()

    # empty lists to store data
    likes = []
    dislikes = []
    views = []
    comments = []

    # loop through stats
    for stat in stat_response['items']:
        try:
            likes.append(stat['statistics']['likeCount'])
        except KeyError:
            likes.append(0)
        try:
            dislikes.append(stat['statistics']['dislikeCount'])
        except KeyError:
            dislikes.append(0)
        try:
            views.append(stat['statistics']['viewCount'])
        except KeyError:
            views.append(0)
        try:
            comments.append(stat['statistics']['commentCount'])
        except KeyError:
            comments.append(0)

    # get channel titles
    snip_request = youtube.videos().list(
        part = 'snippet',
        id = related_Ids)
    snip_response = snip_request.execute()

    # lists for titles
    channels = []
    #titles = []
    upload_date = []

    # loop through snippets
    for snip in snip_response['items']:
        try:
            channels.append(snip['snippet']['channelTitle'])
        except:
            channels.append('api_error')
        #titles.append(snip['snippet']['title'])
        try:
            upload_date.append(snip['snippet']['publishedAt'])
        except:
            upload_date.append('api_error')

    # add fields to dataframe
    #fields = [durations, likes, dislikes, views, comments]
    df = pd.DataFrame()
    df['Title'] = in_df['Title']
    df['Channel'] = channels
    df['Length'] = durations
    df['Likes'] = likes
    df['Dislikes'] = dislikes
    df['Views'] = views
    #df['LikeRatio'] =
    df['Comments'] = comments
    df['Uploaded'] = upload_date
    df['Depth'] = in_df['depth']

    # convert to int
    fields = ['Likes', 'Dislikes', 'Views', 'Comments']
    #fields = ['Likes', 'Dislikes', 'Views']
    for field in fields:
        df[field] = df[field].apply(lambda x: int(x))

    # create LikeRatio
    df['LikeRatio'] = df['Likes'] / (df['Likes'] + df['Dislikes'])
    return df

def get_video_data(df):
    """ The youtube api only lets you submit 50 links at a time
    (as far as I know) so this function addresses that"""
    out_df = pd.DataFrame()
    for i in range(0,len(df)-50,50):
        temp = related_api_requests(df[i:i+50])
        out_df = out_df.append(temp)
    # verbose way to get the starting index of the remainder
    remainder = len(df) - (len(df) % 50)
    temp = related_api_requests(df[remainder:remainder + len(df) % 50])
    out_df = out_df.append(temp)
    index = [i for i in range(len(out_df))]
    out_df['index'] = index
    return out_df

def rabbit_hole(url, channel_name):
    """This function actually handles the surfing of YouTube.
    It also controls the maximum number of videos "deep" a rabbit hole
    could go."""
    chrome_options = Options()
    #chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(executable_path = 'chromedriver_linux64/chromedriver', options = chrome_options)

    final_df = pd.DataFrame()
    selected_ids = []
    ctr = 0

    driver.get(url)
    # max number of videos
    for i in range(50):
        # go to selected video
        #driver.get(url)
        # get video title, link, and id
        df = get_related_data(driver)
        # add depth
        df['depth'] = i
        # append to output dataframe
        final_df = final_df.append(df)
        # select next video (random)
        # selected video is at top of df, so we start at 1 to avoid repeats
        rand = random.randint(1, len(df) - 1)
        #url = df['Link'][rand]
        # getting the proper xpath. I tried using backslash for a newline, but it doesn't work within the
        # function for some reason. it works in the cell above...something to do with jupyter maybe?
        vid1 = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[12]/ytd-watch-"
        vid2 = "next-secondary-results-renderer/div[2]/ytd-compact-video-renderer[" + str(rand) + "]/div[1]/div/div[1]/a/h3/span"
        vid = vid1 + vid2
        selected = driver.find_element_by_xpath(vid)
        # sometimes the click method gives an ElementClickInterceptedException, so this is an
        # attempt to handle that exception. just go straight to the url instead of clicking on the video.
        try:
            selected.click()
        except:
            driver.get(df['Link'][rand])
        #selected_ids.append(rand + ctr)
        #ctr += len(df)
        # keep it on the same channel, the official one for the show. if the channel isn't the official one,
        # end the loop, as the user has exited the channel's sphere of influence
        channel = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[9]/div[2]/ytd-video-secondary-info-renderer/div/div/ytd-video-owner-renderer/div[1]/ytd-channel-name/div/div/yt-formatted-string/a')
        name = channel.text
        if name != channel_name:
            break
        selected_ids.append(rand + ctr)
        ctr += len(df)
    #driver.quit()
    # manually add an index because the append method starts the
    # index at 0 for every temp df added
    index = [i for i in range(len(final_df))]
    final_df['index'] = index
    return final_df, selected_ids

def generate_data(url, channel):
    """This function controls how many rabbit holes to create and makes
    the dictionaries that contain all of the data from the rabbit holes."""
    data_dict = {}
    selected_dict = {}
    for i in range(100):
        # go down the rabbit hole, current max of 50 vids (changed to 10)
        df, selected = rabbit_hole(url, channel)
        # get metrics like views, comments, date, likes, dislikes
        full_df = get_video_data(df)
        # isolate the videos that were actually 'clicked' on
        selected_df = full_df[full_df['index'].isin(selected)]
        data_dict[i] = full_df
        selected_dict[i] = selected_df
        print(i)
    return data_dict, selected_dict
