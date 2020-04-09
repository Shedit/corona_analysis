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

def px_plot_hist_jhop(df, amount = 10000):

    today = dt.date.today() 
    today = today.strftime("%-m/%-d/%y")

    cases = df[(df['type'] == 'confirmed')]
    deaths = df[(df['type'] == 'deaths')]
    recovered = df[(df['type'] == 'recovered')]
    #fig = px.bar(cases, x='country', y='value')
    #condition = cases['value'] >= 10000

    cases = cases[cases['value'] >= amount]
    deaths = deaths[deaths['country'].isin(cases['country'])]
    recovered = recovered[recovered['country'].isin(cases['country'])]
    cases['sub_cases'] = cases['value'].values - (deaths['value'].values + recovered['value'].values)
    
    fig = go.Figure(
        go.Bar(
            x=deaths.country, y=deaths.value, name = 'Deaths', marker_color = 'red'
        ),

        layout_title_text = 'All countries with over {} cases'.format(amount),

     )
    fig.add_trace(
        go.Bar(
            x=recovered.country, y=recovered.value, name = 'Recovered', marker_color = 'green'
        )
    )
    fig.add_trace(
        go.Bar(
            x=cases.country, y=cases.value, name = 'Cases', text=cases.value, marker_color = 'blue'
        )
    )

    fig.update_layout({
        'barmode': 'stack',
        })

    return fig

def map_plot(df):
    
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')

    fig = go.Figure(
        data=go.Choropleth
        (
        locations = df['CODE'],
        z = df['GDP (BILLIONS)'],
        text = df['COUNTRY'],
        colorscale = 'Blues',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '$',
        colorbar_title = 'GDP<br>Billions US$',
    )
    )

    fig.update_layout(
        
        title_text='2014 Global GDP',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        annotations = [dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
                CIA World Factbook</a>',
            showarrow = False
        )]
    )

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

def log_trend_all(df, toplimit = 100):
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

    largest_cases_array = testdf.nlargest(toplimit, ['value']).loc[:, 'country'].values

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

    #fig = px.line(newdf, x='value', y='newCases', color='continent', log_x= True, log_y= True, hover_name='country')

    fig = go.Figure()

    for data in newdf.groupby('country'):
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

    def get_country():

        client = cor.Client()

        obj = await (client.get_all_countries())
        
        await client.request_client.session.close()

        return obj


    data_list = get_country()

    df = pd.DataFrame([(i.__dict__) for i in data_list])

    df['iso3'] = pd.DataFrame([i.info.iso3 for i in data_list])

    df2 = pd.read_csv('data/all_countries_by_continent.csv')
    df2.columns = df2.columns = [i.lower() for i in df2.columns.values]

    df = pd.merge(df, df2, left_on='iso3', right_on='iso-alpha3 code', how='outer')
    country_is_null_in_df2 = df[pd.isnull(df['country or area'])]['name']
    country_is_null_in_df = df[pd.isnull(df['name'])]['country or area']

    df = df.dropna(how='any', subset= ['name', 'country or area'])

    df = df.loc[df['cases'] >= 5000]
    # make other countries below 5000 cases other, sorted by continent
    df = df.loc[:, ['continent','name', 'active', 'recoveries','deaths']]

    sunburst = df.melt(id_vars=(['continent', 'name']))

    fig = px.sunburst(sunburst, path=['continent', 'name', 'variable'], values='value')
    fig.update_layout(title='Countries over 5000 cases')
    return fig