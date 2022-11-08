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
import pickle


## Title

st.title("Prediction of MLB Players' Batting Average")

mlb_df = pd.read_csv('project_csv.csv')

## Graphing and Buttons streamlit

st.write(
'''
### Histogram of MLB Baseball batters bewteen 1998 - 2021
'''
)

fig, ax = plt.subplots()
plt.xlabel('Batting Average')
plt.ylabel('Number of Players')
ax.hist(mlb_df['BA'])
ax.set_title('Distribution of Batting average')

show_graph = st.pyplot(fig)



lr = pickle.load(open('project_pkl.pkl','rb'))
X_test = pickle.load(open('X_test.pkl','rb'))
y_test = pickle.load(open('y_test.pkl','rb'))

st.write(
'''
## R_Squared Number of trained model
'''
)

st.write(f'Test RÂ²: {lr.score(X_test, y_test):.3f}')

# Predictions from User Input

st.write(
'''
## Prediction of Batting Average
'''
)


age_1 = st.number_input('Age', value = 22)
game_played_1 = st.number_input('Game_Played', value =152)
pa_1 = st.number_input('PA', value = 598) 
at_bat_1 = st.number_input('At_Bat', value = 535)
run_1 = st.number_input('Run', value = 65)
hit_1 = st.number_input('Hit', value = 124)
double_1 = st.number_input('Double', value =22)
homerun_1 = st.number_input('Homerun', value = 14)
rbi_1 = st.number_input('RBI', value = 60)
so_1 = st.number_input('SO', value=95)
bb_1 = st.number_input('BB', value=56)



input_data = pd.DataFrame({'Age' : [age_1],
                          'Game_Played' : [game_played_1], 'PA' : [pa_1],
                         'At_Bat' : [at_bat_1], 'Run' : [run_1], 
                         'Hit' : [hit_1], 'Double' : [double_1],
                         'Homerun' : [homerun_1], 'RBI' : [rbi_1], 'SO' : [so_1], 'BB' : [bb_1]})
pred = lr.predict(input_data)[0]

st.dataframe(input_data)
st.write(
f'Predicted Batting Average:{float(pred):,}'
)




