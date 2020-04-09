import corona_api as cor
import asyncio
import pandas as pd
import numpy as np
#$$ 


client = cor.Client()

data_list = await (client.get_all_countries())
    
await client.request_client.session.close()



df = pd.DataFrame([(i.__dict__) for i in data_list])


df['iso3'] = pd.DataFrame([i.info.iso3 for i in data_list])

df2 = pd.read_csv('~/personal_projects/corona_virus/data/all_countries_by_continent.csv')
df2.columns = df2.columns = [i.lower() for i in df2.columns.values]

df = pd.merge(df, df2, left_on='iso3', right_on='iso-alpha3 code', how='outer')

country_is_null_in_df2 = df[pd.isnull(df['country or area'])]['name']
country_is_null_in_df = df[pd.isnull(df['name'])]['country or area']

df = df.dropna(how='any', subset= ['name', 'country or area'])


print('null in df:', country_is_null_in_df)
print('nul in df2:', country_is_null_in_df2)
print(df.columns)

print(df.loc[pd.isnull(df['continent'])])

df = df.loc[:, ['continent','name', 'active', 'recoveries','deaths']]

sunburst = df.melt(id_vars=(['continent', 'name']))

sunburst = sunburst.groupby(['continent', 'name', 'variable']).sum().reset_index()

### Getting ID-list for sunburst continents -> continents_name -> continents_name_variable 
ids = []
ids.append(list(sunburst.continent.unique()))
ids.append(list((sunburst.continent + '_' + sunburst.name).unique()))
ids.append(list(sunburst.name + '_' + sunburst.variable))
# merge continent, name and variable together

# chains to dezip nested list 
import itertools
flat_ids= list(itertools.chain.from_iterable(ids))

ids = flat_ids 

print(len(flat_ids))
        
#labels continents -> name -> variable 

labels = []
labels.append(list(sunburst.continent.unique()))
labels.append(list(sunburst.name.unique()))
labels.append(list(sunburst.variable))

flat_labels= list(itertools.chain.from_iterable(labels))

labels = flat_labels 

print('labels: {}'.format(len(labels)), 'ids: {}'.format(len(ids)))

###parents = "" "" "" for all continents, + continents for all names

parents = []
parents.append(["" for i in sunburst.continent.unique()])
parents.append(list((sunburst.continent + '_' + sunburst.name).unique()))
parents.append(list(sunburst.continent + '_' + sunburst.name))

flat_parents= list(itertools.chain.from_iterable(parents))


parents = flat_parents 

print('parents: {}'.format(len(parents)),'labels: {}'.format(len(labels)), 'ids: {}'.format(len(ids)))

## 

grouped_sun_by_continent = sunburst.groupby('continent').sum()
grouped_sun_by_name = sunburst.groupby('name').sum()
grouped_sun_by_continent_name_variable = sunburst.groupby(['continent', 'name','variable']).sum()
values = []
values.append(list(grouped_sun_by_continent['value']))
values.append(list(grouped_sun_by_name['value']))
values.append(list(grouped_sun_by_continent_name_variable['value']))


flat_values= list(itertools.chain.from_iterable(values))

values = flat_values 

print('values: {}'.format(len(values)),'parents: {}'.format(len(parents)),'labels: {}'.format(len(labels)), 'ids: {}'.format(len(ids)))

merged_list = []
merged_list.append(ids)
merged_list.append(labels)
merged_list.append(parents)
merged_list.append(values)
merged_df = pd.DataFrame(merged_list).transpose()

merged_df.columns = ['ids', 'labels', 'parents', 'values']

merged_df.loc[merged_df.index[0:216], 'parents'] = merged_df.loc[merged_df.index[0:216], 'parents'].str.split('_').str[0]

print(merged_df)
import plotly.graph_objects as go

fig =go.Figure(go.Sunburst(
  ids= merged_df.ids,
  labels= merged_df.labels,
  parents= merged_df.parents,
  values= merged_df.values
))
fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))

fig.show()