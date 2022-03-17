from __future__ import division, print_function
import requests, bs4
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import (cross_val_score, train_test_split, 
                                     KFold, GridSearchCV)
import streamlit as st

##  Making URL list to scrape data
url = 'https://www.baseball-reference.com/teams/{}/{}'
team_list = ['ATL', 'PHI', 'NYM', 'MIA', 'WSN', 'MIL', 'STL', 'CIN', 'CHC',
            'PIT', 'SFG', 'LAD', 'SDP', 'COL', 'ARI', 'TBR', 'NYY', 'BOS',
            'TOR', 'BAL', 'CHW', 'CLE', 'DET', 'KCR', 'MIN', 'HOU', 'SEA', 
            'OAK', 'LAA', 'TEX']
url_list = []

year_list = [*range(1998, 2022, 1)]
year_list = [str(x) for x in year_list]

for t in year_list:
    url = 'https://www.baseball-reference.com/teams//' + t + '.shtml'
    for i in team_list:


        ## MON to WSN
        if i == 'WSN' and int(t) < 2005:
            i = 'MON'
            
        ## TBD to TBR
        if i == 'TBR' and int(t) < 2008:
            i ='TBD'
        
        ## FLA to MIA
        if i == 'MIA' and int(t) < 2012:
            i = 'FLA'
        
        ## ANA to LAA
        if i == 'LAA' and int(t) < 2005:
            i = 'ANA'
            
        
        team_temp = url[:41] + i + url[41:]
        url_list.append(team_temp)

## function to help scraping
def delete_let(a, b):
    num_let = a.count(b)
    i = 0
    while i < num_let:
        a.remove(b)
        i += 1
    return a

## scraping data
player_list = []

age_f = []
game_played_f = []
pa_f = []
at_bat_f = []
runs_f = []
hits_f = []
doubles_f = []
homeruns_f = []
so_f = []
bb_f = []
ba_f = []
rbi_f = []


for u in url_list:
    soup = bs(requests.get(u).text)

    spex = soup.find('tbody')

    #age
    age_tag = spex.find_all(attrs = {'data-stat' : 'age'})
    age = [t.text for t in age_tag]
    delete_let(age, 'Age')
    age_f.extend(age)
#     print(age)


    #Game played
    game_played_tag = spex.find_all(attrs = {'data-stat' : 'G'})
    game_played = [t.text for t in game_played_tag]
    delete_let(game_played, 'G')
    game_played_f.extend(game_played)
#     print(game_played)

    #Plate Appearances
    pa_tag = spex.find_all(attrs = {'data-stat' : 'PA'})
    pa = [t.text for t in pa_tag]
    delete_let(pa, 'PA')
    pa_f.extend(pa)
#     print(pa)

    #At Bats
    at_bat_tag = spex.find_all(attrs = {'data-stat' : 'AB'})
    at_bat = [t.text for t in at_bat_tag]
    delete_let(at_bat, 'AB')
    at_bat_f.extend(at_bat)
#     print(at_bat)

    #Runs Scored
    runs_tag = spex.find_all(attrs = {'data-stat' : 'R'})
    runs = [t.text for t in runs_tag]
    delete_let(runs, 'R')
    runs_f.extend(runs)
#     # print(runs)

    #Hits
    hits_tag = spex.find_all(attrs = {'data-stat' : 'H'})
    hits = [t.text for t in hits_tag]
    delete_let(hits, 'H')
    hits_f.extend(hits)
#     # print(hits)

    #Doubles Hit
    doubles_tag = spex.find_all(attrs = {'data-stat' : '2B'})
    doubles = [t.text for t in doubles_tag]
    delete_let(doubles, '2B')
    doubles_f.extend(doubles)
#     # print(doubles)

    #Home Runs
    homeruns_tag = spex.find_all(attrs = {'data-stat' : 'HR'})
    homeruns = [t.text for t in homeruns_tag]
    delete_let(homeruns, 'HR')
    homeruns_f.extend(homeruns)
#     # print(homeruns)

    #Runs Batted In
    rbi_tag = spex.find_all(attrs = {'data-stat' : 'RBI'})
    rbi = [t.text for t in rbi_tag]
    delete_let(rbi, 'RBI')
    rbi_f.extend(rbi)
#     print(rbi)

    #Strikeouts
    so_tag = spex.find_all(attrs = {'data-stat' : 'SO'})
    so = [t.text for t in so_tag]
    delete_let(so, 'SO')
    so_f.extend(so)
#     # print(so)

    #Bases on Balls
    bb_tag = spex.find_all(attrs = {'data-stat' : 'BB'})
    bb = [t.text for t in bb_tag]
    delete_let(bb, 'BB')
    bb_f.extend(bb)
#     # print(bb)

    #Batting Averages - target
    batting_avg_tag = spex.find_all(attrs = {'data-stat' : 'batting_avg'})
    batting_avg = [t.text for t in batting_avg_tag]
    delete_let(batting_avg, 'BA')
    ba_f.extend(batting_avg)
#     print(batting_avg)

## Cleaning at_bat data to make it standard

for i in range(0, len(at_bat_f)):
    if at_bat_f[i] == '':
        at_bat_f[i] = 'n/a'


## Setting mlb_df columns
mlb_df = pd.DataFrame(list(zip(age_f, game_played_f, pa_f, at_bat_f, 
                              runs_f, hits_f, doubles_f, homeruns_f, rbi_f,
                              so_f, bb_f, ba_f)), 
                      columns = ['Age', 'Game_Played', 'PA', 'At_Bat',
                                'Run', 'Hit', 'Double', 'Homerun', 'RBI',
                                'SO', 'BB', 'BA'])



#data cleaning

mlb_df['At_Bat']
mlb_df = mlb_df.loc[mlb_df['At_Bat'] != 'n/a']

mlb_df['At_Bat'] = mlb_df['At_Bat'].astype(int)

mlb_df = mlb_df.loc[mlb_df['At_Bat'] >= 162]

## Changing data typep of each columns

mlb_df['Age'] = mlb_df['Age'].astype(int)
mlb_df['Game_Played'] = mlb_df['Game_Played'].astype(int)
mlb_df['PA'] = mlb_df['PA'].astype(int)
mlb_df['Run'] = mlb_df['Run'].astype(int)
mlb_df['Hit'] = mlb_df['Hit'].astype(int)
mlb_df['Double'] = mlb_df['Double'].astype(int)
mlb_df['Homerun'] = mlb_df['Homerun'].astype(int)
mlb_df['RBI'] = mlb_df['RBI'].astype(int)
mlb_df['SO'] = mlb_df['SO'].astype(int)
mlb_df['BB'] = mlb_df['BB'].astype(int)
mlb_df['BA'] = mlb_df['BA'].astype(float)

## Graphing and Buttons streamlit

st.write(
'''
### Graphing and Buttons
Let's graph some of our data with matplotlib. We can also add buttons to add interactivity to our app.
'''
)

fig, ax = plt.subplots()

ax.hist(mlb_df['BA'])
ax.set_title('Distrivution of Batting average')

show_graph = st.checkbox('Show Graph', value=True)

if show_graph:
    st.pyplot(fig)


# PART 6 - Linear Regression Model

st.write(
'''
## Train a Linear Regression Model
Now let's create a model to predict batting averages from other statistics.
'''
) 

X = mlb_df.drop(columns = 'BA')
y = mlb_df['BA']


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

lr = LinearRegression()
lr.fit(X_train, y_train)

st.write(f'Test RÂ²: {lr.score(X_test, y_test):.3f}')



