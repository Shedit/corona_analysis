import numpy as np 
import pandas as pd 
import pprint as pp
def tidy_historical(data):
    data = add_country_data(data)
    data = column_merge_country_province(data)
    data = data.set_index('countryANDprovince')
    data.columns = ['timeline.cases', 'timeline.deaths', 'timeline.recovered', 'country_or_area', 'iso-alpha3 code',
       'm49 code', 'region 1', 'region 2', 'continent']

    cases_unpack_list = ((k,'cases', i[0], i[1],data.loc[k,'country_or_area'], data.loc[k,'continent']) for k in data.index \
              for i in data.loc[k, 'timeline.cases'].items())
    deaths_unpack_list = ((k,'deaths', i[0], i[1], data.loc[k,'country_or_area'], data.loc[k,'continent']) for k in data.index \
              for i in data.loc[k, 'timeline.deaths'].items())
    recovered_unpack_list = ((k,'recovered', i[0], i[1], data.loc[k,'country_or_area'], data.loc[k,'continent']) for k in data.index \
              for i in data.loc[k, 'timeline.recovered'].items())    

    b_list = []

    for i in cases_unpack_list:
        b_list.append(i)
    for i in deaths_unpack_list:
        b_list.append(i)
    for i in recovered_unpack_list:
        b_list.append(i)

    df_tidy = pd.DataFrame(b_list, columns = ['country', 'type', 'date', 'value', 'country_or_area', 'continent'])
    df_tidy['value'] = df_tidy['value'].astype(int) 
    return df_tidy

def tidy_stats_jhopkins(data):

    data = column_merge_country_province(data)
    data = data.set_index('countryANDprovince')

    c_list = [(k,i,j) for k in data.index \
             for i, j in data.loc[k, 'stats'].items()]
    
    del data
    
    df_tidy = pd.DataFrame(c_list, columns = ['country', 'type', 'value'])
    
    return df_tidy

def column_merge_country_province(data):

    a_list = [i for i in data.loc[:, 'country']]
    data['countryANDprovince'] = a_list

    for i, content in enumerate(data.loc[:,'province']):
        if content == None:
            pass 
        else:
            content = " " + content
            data.loc[data.index[i], 'countryANDprovince'] += content

    del data['country']
    del data['province']
    # set new col first 

    b_list = []
    b_list.append(data.columns[-1])
    for i in data.columns[0: -1]:
        b_list.append(i)

    data = data[b_list]

    return data 

def add_country_data(df):

    df2 = pd.read_csv('data/all_countries_by_continent.csv')
    df2.columns = [i.lower() for i in df2.columns.values]
    merged = pd.merge(df, df2, left_on= 'country', right_on='country or area')
    merged = merged.dropna(how='any', subset=['timeline.cases', 'timeline.deaths', 'timeline.recovered'])

    return merged

def count_sum_of_nested_dicts(df, col, nestkey):

    a_gen = (df.loc[i, col] for i in df.index)
    b_gen = (i[nestkey] for i in a_gen)
    
    return sum(b_gen)

def melted_growth_ratio(df):
    # expects tidy historical
    return

def get_cases_by_continent(df):

    df = df.loc[(df['type']== 'cases')]

    df = df.groupby('country')

    list_a = [(j.loc[j.index[-1], 'continent'], j.loc[j.index[-1], 'value']) for i, j in df]
  
    df = pd.DataFrame(list_a, columns = ['continent', 'value'])

    df = df.groupby('continent').sum()

    return df
