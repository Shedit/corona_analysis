#%%
from API.call_functions import *
from graph_functions import *
from cleaning_functions import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


call = calls()

data_json = call.historical()

data = pd.read_json(data_json)

#%%
data['countryANDprovince'] = np.nan
for i, content in enumerate(data['country']):
    data['countryANDprovince'][i] = content

for i, content in enumerate(data['province']):
    if content == None:
        pass 
    else:
        content = " " + content
        data['countryANDprovince'][i] += content
del data['country']
del data['province']

#%%
## get a data frame with timeseries having cases, deaths, recovered  
for i, lists in enumerate(data['timeline']):
    data['timeline'][i] = pd.DataFrame(lists)

data = data[['countryANDprovince', 'timeline']]

#%% 

for i, content in enumerate(data['timeline']):
    data['timeline'][i]['countrySegment'] = np.nan
    data['timeline'][i]['countrySegment'] = data['countryANDprovince'][i]
    data['timeline'][i].reset_index()


#%%
    df = pd.DataFrame()
    for i, content in enumerate(data['timeline']):
        df = df.append(data['timeline'][i])
        print(i, "done")


#%%

import plotly.express as px

#df2 = df.reset_index()

df2 = df2.melt(id_vars=['index', 'countrySegment'])
#%%
fig = px.line(df2, x='index', y='value', color='variable', hover_name='countrySegment')
fig.show()

# %%

seperate_pull = data

seperate_pull = seperate_pull.set_index('countryANDprovince', drop = True)

can_on = pd.DataFrame(seperate_pull['timeline']['canada ontario'])

# %%

can_on = can_on.reset_index()

can_on = can_on.melt(id_vars="index")
#%%
import plotly.express as px

fig2 = px.line(can_on, x='index', y='value', color='variable')
fig2.show()

# %%
testdf = call.historical(country = 'Canada')

testdf = pd.read_json(testdf)
# %%

testdf['timeline']['cases']

# %%
can = requests.get('https://corona.lmao.ninja/v2/historical/canada')
can = can.json()
can = pd.DataFrame(can['timeline'])
can = can.reset_index()
can = can.melt(id_vars='index')
# %%
fig2 = px.line(can, x='index', y = 'value', color='variable')
fig2.show()




# %%

quickplot_country('america')



# %%
import requests 
import pandas as pd 
from cleaning_functions import *


df3 = requests.get('https://corona.lmao.ninja/v2/historical')
df3 = df3.text
df3 = pd.read_json(df3)
df3 = column_merge_country_province((df3))
df3 = df3.set_index('countryANDprovince')

b_list = [(k,i,j,m) for k in df3.index for i in df3.loc[k, 'timeline'].keys() for j, m in df3.loc[k, 'timeline'][i].items()]

df_tidy = pd.DataFrame(b_list, columns = ['country', 'type', 'date', 'value'])



#%% 
import plotly.express as px
fig2 = px.line(df_tidy, x='date', y = 'value', color='type')
fig2.show()




# %%

from cleaning_functions import *

test = tidy_historical(data)

# %%
def tidy_historical(data):

    data = column_merge_country_province((data))
    data = data.set_index('countryANDprovince')

    b_list = [(k,i,j,m) for k in data.index \
             for i in data.loc[k, 'timeline'].keys() \
             for j, m in data.loc[k, 'timeline'][i].items()]
    
    del data
    
    df_tidy = pd.DataFrame(b_list, columns = ['country', 'type', 'date', 'value'])
    
    return df_tidy

# %%
test = tidy_historical(data)