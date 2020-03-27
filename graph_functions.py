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

def px_plot_hist(df):

    yesterday = dt.date.today() - dt.timedelta(days=1)
    yesterday = yesterday.strftime("%-m/%-d/%y")

    cases = df[(df['date'] == yesterday) & (df['type'] == 'cases')]
    deaths = df[(df['date'] == yesterday) & (df['type'] == 'deaths')]
    

    # fig = go.Figure(data=[
    #     go.Bar(name='Deaths', x=x_all, y=deaths_values),
    #     go.Bar(name='Cases', x=x_all, y=cases_values)
    # ])
    
    # Change the bar mode
    #fig.update_layout(barmode='stack')
    
    fig = px.bar(cases, x='country', y='value')
    
  

    return fig