import os
import requests
import datetime as dt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def px_line_plot(df, country):
   
    df = df.loc[df['country'] == country]

    fig = px.line(df, x='date', y = 'value', color='type', title = country )

    return fig 

def px_plot_hist(df, amount = 1):

    today = dt.date.today() 
    today = today.strftime("%-m/%-d/%y")

    cases = df[(df['date'] == today) & (df['type'] == 'cases')]
    deaths = df[(df['date'] == today) & (df['type'] == 'deaths')]
    
    if (cases['value'].count() < 10):
        yesterday = dt.date.today() - dt.timedelta(days=1)
        yesterday = yesterday.strftime("%-m/%-d/%y")
        cases = df[(df['date'] == yesterday) & (df['type'] == 'cases')]
        deaths = df[(df['date'] == yesterday) & (df['type'] == 'deaths')]

    #fig = px.bar(cases, x='country', y='value')
    #condition = cases['value'] >= 10000
    
    cases = cases[cases['value'] >= amount]
    deaths = deaths[deaths['country'].isin(cases['country'])]

    fig = px.bar(cases, x='country', y='value', title = 'All countries with over {} cases'.format(amount))

    fig.add_trace(go.Bar(x=deaths.country, y=deaths.value, name = 'Deaths'))

    fig.update_layout(
        barmode="overlay",
        bargap=0.1)

    return fig