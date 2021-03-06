import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc
import datetime as dt
import time
import math

from graph_functions import * 
from cleaning_functions import *
from API.call_functions import *

# Data Imports 

API = calls()
df_hist = pd.DataFrame()
df_jhopkins = pd.DataFrame()
tidy_stats_jhop = pd.DataFrame()
total_stats = pd.DataFrame()

def total_import():
    global total_stats
    total_stats = API.all()

total_import()

def data_imports():

    global df_hist
    global tidy_stats_jhop
    global df_jhopkins

    data_hist_json = API.historical()
    df_hist = pd.DataFrame(pd.json_normalize(data_hist_json, max_level=1))
    df_hist = tidy_historical(df_hist)

    data_jhopkins_json = API.jhopkins()
    df_jhopkins = pd.read_json(data_jhopkins_json)
    df_jhopkins['updatedAt'] = pd.to_datetime(df_jhopkins['updatedAt'])

    tidy_stats_jhop = tidy_stats_jhopkins(df_jhopkins)

data_imports()


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.DARKLY]
)

server = app.server

colors = {
    'background': '#333',
    'text': '#7FDBFF',
    'paper': '#333',
    'sun': '#222'
}

graph_style = {
            'legend': { 'x': 0, 'y': 1},
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['paper'],
            'font': {'color': colors['text']}
            }

sun_style = {
            'legend': { 'x': 0, 'y': 1},
            'plot_bgcolor': colors['sun'],
            'paper_bgcolor': colors['sun'],
            'font': {'color': colors['text']}
            }

def _get_label_dict(bins = 3): 
    global df_jhopkins 
 
    length = df_jhopkins.iloc[:,0].count()
    steps = math.floor(length/bins)
    _list = [math.floor((steps*i)/2) for i in range(1,bins+1)]

    return _list 

app.layout = \
dbc.Container(
    html.Div(
        children = [
        html.Div(
            children=[
            html.H1(children='COVID-19',
                style={
                        'test-align': 'center'
                    }),

            html.Div(children=
                html.H3('A presentation of data related to COVID-19.'),
            style={
                'test-align': 'center'
                    }),
            dbc.Container(
                dcc.Graph(
                    id='sunburst',
                    figure = sunburst_plot().update_layout(sun_style)
                )
            ),
            dbc.Container(
                dbc.CardColumns(
                    html.Div(children =[
                        dbc.Card(
                            dbc.CardBody(
                                [html.Header('{}'.format(i)),       
                                    html.P(
                                            '{}'.format(j), className='card-text', id = i   
                                    )]
                                
                            ), color = 'secondary'
                        )
                    for i, j in total_stats.items() if i not in ['updated', 'deathsPerOneMillion', 'deathsPerOneMillion', 'casesPerOneMillion', 'testsPerOneMillion', 'continent']],
                    )    
                )
            ),

            html.Div(children = [
                html.P('Data last updated {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(total_stats['updated']/1000))))
                ],
                style = { 'text-align': 'center'}
            ),
################################################## BAR-GRAPH            
            html.Div(children= [
                dcc.Graph(
                    id='hist-tot-cases-by-country',
                    figure=  px_plot_hist_jhop(tidy_stats_jhop).update_layout(graph_style)
                ),

                dcc.RadioItems(
                    id="radio",
                    options = [{'label': str(10**i), 'value': 10**i } \
                            for i in range(0,5)],
                    value = 10000, 
                )
            ]),
##################################################### LOG-TREND-GRAPH 
            html.Div(children= [
                dcc.Graph(
                    id='log-plot-all',
                    figure= log_trend_all(df_hist, _get_label_dict()[0], 'cases').update_layout(graph_style, showlegend = False)
                ),
                dcc.
                RadioItems(
                    id="radio-log",
                    options = [{'label': str(i), 'value': i } \
                            for i in _get_label_dict()],
                    value = _get_label_dict()[0], 
                ),
                dcc.
                RadioItems(
                    id="radio-log-type",
                    options = [{'label': 'Cases', 'value': 'cases'},
                               {'label': 'Deaths', 'value': 'deaths'},
                               {'label': 'Recovered', 'value': 'recovered'}],
                    value = 'cases', 
                )                
                
            ]),
##################################################### LINE-GRAPHS WITH DROPDOWN MENU
                html.Div(children=[
                    html.Div(children = [
                            dcc.Dropdown(
                                id="drop",
                                options=[{'label': i, 'value': i } \
                                        for i in df_hist.loc[:, 'country'].unique()],
                                        value = 'Canada ontario',
                                        style={
                                            'width':'40%',
                                            'display':'inline-block',
                                            'verticalAlign':"middle",
                                            'background': colors['background']
                                        }
                        )
                    ])
                ]),    
###################################################### Line plots per country                    
                dbc.Container(
                    dbc.Row([
                        dbc.Col(
                            html.Div(children = [
                                dcc.Graph(
                                    id='px-line-plot',
                                    figure= px_line_plot(df_hist, 'Canada ontario').update_layout(graph_style),     
                                )]
                            ),
                        className="md-6"
                        ), 
                        dbc.Col(
                            html.Div(children= [
                                dcc.Graph(
                                    id='px-line-plot-ratio',
                                    figure= px_line_plot_ratio(df_hist, 'Canada ontario').update_layout(graph_style)
                                )]
                            ),
                        className="md-6"
                        )
                    ])
                ),
            html.Div(children = [
                    dcc.Markdown('''
                    ##### Sources
                    Data supported from https://github.com/novelcovid/api
                    ''', style={'text-align':'left'})
            ]),
        ])
    ])
)



@app.callback(
    Output('hist-tot-cases-by-country', 'figure'),
    [Input('radio', 'value')])
def update_hist_div(value):
    return px_plot_hist_jhop(df = tidy_stats_jhop, amount = value).update_layout(graph_style)

@app.callback(
    Output(component_id='px-line-plot', component_property='figure'),
    [Input(component_id='drop', component_property='value')])
def update_output_div(input_value):
    return px_line_plot(df_hist, input_value).update_layout(graph_style)

@app.callback(
    Output(component_id='px-line-plot-ratio', component_property='figure'),
    [Input(component_id='drop', component_property='value')])
def update_output_div(input_value):
    return px_line_plot_ratio(df_hist, input_value).update_layout(graph_style)

@app.callback(
    Output('log-plot-all', 'figure'),
    [Input('radio-log', 'value'),
    Input('radio-log-type', 'value')])
def update_log_trend(log_value, log_type_value):
    return log_trend_all(df_hist, log_value, log_type_value).update_layout(graph_style, showlegend = False)
# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)

