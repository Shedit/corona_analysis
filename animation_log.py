from API.call_functions import *
from graph_functions import *
from cleaning_functions import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


call = calls()

df = call.historical()

df = pd.read_json(df)

df = tidy_historical(df)


test = df.loc[df['type'] == 'cases']

test.loc[:, 'newCases'] = test.groupby('country')['value'].diff()

# Getting largest values 
grouped_test = test.groupby('country')

# Get the latest value from date for each country 
a_list = [i[1].loc[i[1].loc[:, 'date'] == (dt.datetime.today() - dt.timedelta(days=1)).strftime("%-m/%-d/%y")] for i in grouped_test]

testdf = pd.DataFrame()

for i in a_list:
    testdf = testdf.append(i)

#Saving the names of the countires of the largest amount of cases

largest_cases_array = testdf.nlargest(50, ['value']).loc[:, 'country'].values

# Getting countries with the largest amount of cases 
plot_df = test.loc[test.loc[:, 'country'].isin(largest_cases_array)]

# Getting all grouped dataframes 

b_list = [i for i in plot_df.groupby('country')]

newdf = pd.DataFrame()

for i, df in b_list:
    df = df.reset_index(drop = True)
    val = df.loc[df.index[1], 'newCases'] - df.loc[df.index[0], 'newCases']
    df.loc[:, 'newCases'] = df.loc[:, 'newCases'].rolling(window=5).mean()
    df = df.fillna(val)

    newdf = newdf.append(df)

newdf = newdf.reset_index(drop = True)

fig = px.line(newdf, x='value', y='newCases', color='continent', log_x= True, log_y= True, hover_name = 'country', animation_frame='date', animation_group='country', range_x=[1,150000], range_y=[1,15000])

fig.update_layout(showlegend=False)

fig.animation
fig.show()