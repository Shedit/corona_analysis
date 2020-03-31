import numpy as np 
import pandas as pd 

def tidy_historical(data):

    data = column_merge_country_province((data))
    data = data.set_index('countryANDprovince')

    b_list = [(k,i,j,m) for k in data.index \
             for i in data.loc[k, 'timeline'].keys() \
             for j, m in data.loc[k, 'timeline'][i].items()]
    
    del data
    
    df_tidy = pd.DataFrame(b_list, columns = ['country', 'type', 'date', 'value'])
    
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

    b_list = []
    b_list.append(data.columns[-1])
    for i in data.columns[0: -1]:
        b_list.append(i)

    data = data[b_list]
    return data 

def count_sum_of_nested_dicts(df, col, nestkey):

    a_gen = (df.loc[i, col] for i in df.index)
    b_gen = (i[nestkey] for i in a_gen)
    
    return sum(b_gen)

def melted_growth_ratio(df):
    # expects tidy historical
    return

