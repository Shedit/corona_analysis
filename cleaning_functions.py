import numpy as np 
import pandas as pd 


def generate_plot_data(data): 

        return



def column_merge_country_province(data):
    a_list = []
    for i, content in enumerate(data['country']):
        a_list.append(content)

    data['countryANDprovince'] = a_list

    for i, content in enumerate(data['province']):
        if content == None:
            pass 
        else:
            content = " " + content
            data['countryANDprovince'][i] += content

    del data['country']
    del data['province']

    data = data[['countryANDprovince', 'timeline']]

    return data 

## get a data frame with timeseries having cases, deaths, recovered  

def convert_timeline_to_dataframes_ALL(data):
    
    df = pd.DataFrame()
   
    for i, lists in enumerate(data['timeline']):
        
        lists = pd.DataFrame(lists)
        df.append(lists)

    data.timeline.update(df)
       
    
    return data

def convert_timeline_to_dataframes_SINGLE(data):
    data = pd.DataFrame(data['timeline'])
    data = data.reset_index()

    return data 

def melt_country_province(data):
    for i, content in enumerate(data['timeline']):
        data['timeline'][i]['countrySegment'] = np.nan
        data['timeline'][i]['countrySegment'] = data['countryANDprovince'][i]
        data['timeline'][i].reset_index()
    
    df = pd.DataFrame()
    for i, content in enumerate(data['timeline']):
        df = df.append(data['timeline'][i])
    
    del data

    return df



def tidy_historical(data):

    data = column_merge_country_province((data))
    data = data.set_index('countryANDprovince')

    b_list = [(k,i,j,m) for k in data.index \
             for i in data.loc[k, 'timeline'].keys() \
             for j, m in data.loc[k, 'timeline'][i].items()]
    
    del data
    
    df_tidy = pd.DataFrame(b_list, columns = ['country', 'type', 'date', 'value'])
    
    return df_tidy

