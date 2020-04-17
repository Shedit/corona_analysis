import os
import requests
import asyncio
import corona_api as cor
import datetime as dt
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def px_line_plot(df, country):
   
    df = df.loc[df['country'] == country]
    
    numdays = 30 

    base = dt.datetime.today()
    date_list = [(base - dt.timedelta(days=x)).strftime("%-m/%-d/%y") for x in range(numdays)]

    fig = px.line(df, x='date', y = 'value', color='type', title = country )


    return fig 

def px_line_plot_ratio(df, country):
    # It will return a line plot with graph stating a ratio of change to indicate growth
    # Get all 'cases' rows for each country
    # Count Difference for each executive day
    # How much  growth as happened since last growth period?

    df = get_growth_ratio(df, country = country)
  
    growth_today = df['ratio'].tail(1).values 
    
    fig = go.Figure(
        layout=go.Layout(
        legend= { 'x': 1, 'y': 1, 'traceorder': 'normal'},
        title=go.layout.Title(
            text='Growth rate, today growth rate: {}'.format(growth_today)
                )
            )
        )
    fig.add_trace(go.Scatter(x=df.date, y=df.ratio,
                    mode='lines+markers',
                    name='Growth Ratio'))
    fig.add_trace(go.Scatter(x=df.date, y=[0 for i in df.date],
                    mode='lines',
                    name=''))

    return fig


def px_plot_hist_jhop(df, amount = 10000):
    # Main purpose of function: Return a bar plot with the specified data. 

    ## Inner helper functions

    def _get_df_by_type(_type):
    
        nonlocal df 

        _df = df[(df['type'] == _type)]
        
        return _df 

    def _sort_by_amount_cases(_int):

        nonlocal cases
        nonlocal deaths 
        nonlocal recovered 

        _cases = cases[(cases['value'] >= _int)]
        _deaths = deaths[deaths['country'].isin(_cases['country'])]
        _recovered = recovered[recovered['country'].isin(_cases['country'])]

        return _cases, _deaths, _recovered

    def _add_bar_trace(_x, _y, _name, _color): 
        
        nonlocal fig
        
        fig.add_trace(
            go.Bar(
                x=_x, y=_y, name = _name, marker_color = _color
            )
        )

    ###### Outer function

    cases = _get_df_by_type('confirmed')
    deaths = _get_df_by_type('deaths')
    recovered = _get_df_by_type('recovered')
    
    cases, deaths, recovered = _sort_by_amount_cases(amount)

    cases['active_cases'] = cases['value'].values - (deaths['value'].values + recovered['value'].values)
    
    fig = go.Figure()
    
    _add_bar_trace(deaths.country, deaths.value, 'Deaths', 'red')
    _add_bar_trace(recovered.country, recovered.value, 'Recovered', 'green')
    _add_bar_trace(cases.country, cases.active_cases, 'Cases', 'blue')

    fig.update_layout({
        'barmode': 'relative',
        })

    return fig

def map_plot(df):

    fig = None
    return fig 

def get_growth_ratio(df, country = ''):

    if country != '':
        df = df[(df['type'] == 'cases') & (df['country'] == country)]
        df = df.reset_index(drop = True)

    df['past'] = df['value']

    for i, c in df.iterrows():
        
        if( i == max(df.index)):
            pass
        else:     
            df.loc[df.index[i+1],'past'] = c['past']

    df['diff'] = df['value'] - df['past']

    df['ratio'] = df['diff'] / df['past']

    df['ratio'] = df['ratio'].fillna(0)
    df['ratio'] = df['ratio'].replace(np.inf, 1)

    return df

def log_trend_all(df, toplimit = 50):
    
    def _filter_by_cases(df):
        _df = df.loc[df['type']== 'cases']
        return _df
    
    cases = _filter_by_cases(df)

    def _get_new_cases(df):
        _df = df
        _df.loc[:,'newCases'] = df.groupby('country')['value'].diff()
        return _df
    
    cases = _get_new_cases(cases)

    def _sort_by_largest_amount_cases(df, _int = 50): 

        #1. Get latest value for each country and return a dataframe 
        def _get_latest_values():
            nonlocal df 

            _df = df.groupby('country')

            _date_str = (dt.datetime.today() - dt.timedelta(days=1)).strftime("%-m/%-d/%y")
            _list = [country[1].loc[(country[1].loc[:, 'date'] == _date_str)] for country in _df]

            _df = pd.DataFrame()

            for obj in _list:
                _df = _df.append(obj)
            
            return _df

        #2. filter out the nlargest countries and return an array 
        def _filter_top_cases_return_array(df):
            nonlocal _int

            _array = df.nlargest(_int, ['value']).loc[:, 'country'].values

            return _array   

        _df = _get_latest_values()
        top_countries = _filter_top_cases_return_array(_df)

        #3. Get the DataFrame with all countries in top_countires 
        _df = df.loc[df.loc[:, 'country'].isin(top_countries)]

        return _df

    # Getting countries with the largest amount of cases 
    top_cases = _sort_by_largest_amount_cases(cases, toplimit)

    # Getting all grouped dataframes 
    def _smooth_values(df):

        _list = [i for i in df.groupby('country')]

        _df = pd.DataFrame()

        for i, df in _list:
            df = df.reset_index(drop = True)
            val = df.loc[df.index[1], 'newCases'] - df.loc[df.index[0], 'newCases']
            df.loc[:, 'newCases'] = df.loc[:, 'newCases'].rolling(window=5).mean()
            df = df.fillna(val)

            _df = _df.append(df)

        _df = _df.reset_index(drop = True)
    
        return _df 

    result = _smooth_values(top_cases)

    fig = go.Figure()

    for data in result.groupby('country'):
        fig.add_trace(
            go.Scatter(
                x=data[1].value, y=data[1].newCases, mode='lines', line= {'width': 1, 'shape': 'spline'}, name=data[1].country.unique()[0]
            )
        )

    fig.update_xaxes(type="log")
    fig.update_yaxes(type="log")
    fig.update_layout(title="Top {} countries' exponential growth by most confirmed cases".format(toplimit))
    
    return fig

def sunburst_plot():

    async def _get_country():

        client = cor.Client()

        obj = await client.get_all_countries()
        
        await client.request_client.session.close()

        return obj
    
    def _fetch_list_of_objects_from_loop():

        coro = _get_country()
        task = asyncio.ensure_future(coro)
        loop = asyncio.get_event_loop()
        data_list = loop.run_until_complete(task)
        loop.close()
        return data_list 

    def _get_df_from_objects(_list):
        df = pd.DataFrame([(i.__dict__) for i in _list])
        return df    

    def _get_values_from_nested_obj_in_list(_list, col, subcol):
        df = pd.DataFrame([getattr(getattr(i,col), subcol) for i in _list])
        return df 

    def _import_clean_country_data():

        df = pd.read_csv('data/all_countries_by_continent.csv')
        df.columns = df.columns = [i.lower() for i in df.columns.values]
        
        return df 

    def _merge_by_iso3_outer(df, df2):

        df = pd.merge(df, df2, left_on='iso3', right_on='iso-alpha3 code', how='outer')
        
        null_df = df[pd.isnull(df['name'])]['country or area']
        null_df2 = df[pd.isnull(df['country or area'])]['name']

        df = df.dropna(how='any', subset= ['name', 'country or area'])

        return df, null_df, null_df2

    def _filter_by_total_amount_of_cases(df):
        # filter amount of cases and group everything below threshold and name it other for each continent
        # check the for a minimum gap and bin the values to other. 
        # make other countries below 5000  cases other, sorted by continent
        # For all other countries sum the total of all contries, name them other within each continent
       
        def _get_max_gaps_per_continent(df):
            
            _diff = df.groupby(['continent','cases','name']).sum()
            _diff.sort_values('cases')
            _diff = _diff.reset_index(level=1)
            _diff = _diff.diff()
           
            _max = _diff.groupby('continent').max()
            _max = _max.loc[:, 'cases']

            return _max   

        _max = _get_max_gaps_per_continent(df)

        _list = [i for i in df.groupby('continent')]
        result = pd.DataFrame()
        
        for i, c in _list:

            _int = _max[i]

            _df = c[c['cases'] >= _int]
            _rest = c[c['cases'] < _int]

            _rest = _rest.groupby('continent').sum().reset_index()

            _df = _df.append(_rest, ignore_index = True)

            result = result.append(_df, ignore_index = True)
        
        for i, c in result.iterrows():
            if pd.isna(c['name']):
                result.loc[result.index[i], 'name'] = c['continent'] + '_other'   
     
        return result

    def _get_columns_of_interest(*col_names): 
        nonlocal df 

        _list = []
        for name in col_names: 
            _list.append(name)
    
        _df = df.loc[:, _list]

        return _df

#######################

    data_list = _fetch_list_of_objects_from_loop()

    df = _get_df_from_objects(data_list)

    df['iso3'] = _get_values_from_nested_obj_in_list(data_list, 'info', 'iso3')
    
    df2 = _import_clean_country_data()
    
    df, null_first, null_second = _merge_by_iso3_outer(df, df2)
    
    df = _filter_by_total_amount_of_cases(df)
    
    df = _get_columns_of_interest('continent','name', 'active', 'recoveries','deaths')

    sunburst = df.melt(id_vars=(['continent', 'name']))

    fig = px.sunburst(sunburst, path=['continent', 'name', 'variable'], values='value')
    
    fig.update_layout(title='Countries sorted by continents')
    
    return fig


## Scrapped functions but still works 

def px_plot_hist(df, amount = 10000):

    today = dt.date.today() 
    today = today.strftime("%-m/%-d/%y")
    
    cases = df[(df['date'] == today) & (df['type'] == 'active')]
    deaths = df[(df['date'] == today) & (df['type'] == 'deaths')]
    
    if (cases['value'].count() < 10):
        yesterday = dt.date.today() - dt.timedelta(days=1)
        yesterday = yesterday.strftime("%-m/%-d/%y")
        cases = df[(df['date'] == yesterday) & (df['type'] == 'cases')]
        deaths = df[(df['date'] == yesterday) & (df['type'] == 'deaths')]

    
    cases = cases[cases['value'] >= amount]
    deaths = deaths[deaths['country'].isin(cases['country'])]

    fig = px.bar(cases, x='country', y='value', title = 'All countries with over {} cases'.format(amount))

    fig.add_trace(go.Bar(x=deaths.country, y=deaths.value, name = 'Deaths'))

    fig.update_layout({
        'barmode': 'overlay',
        'bargap': 0.1,
        })

    return fig