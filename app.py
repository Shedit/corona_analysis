import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc
import datetime as dt
import time


from graph_functions import * 
from cleaning_functions import *
from API.call_functions import *

# Data Imports 

API = calls()
df_hist = pd.DataFrame()
df_jhopkins = pd.DataFrame()
tidy_stats_jhop = pd.DataFrame()

def data_imports():

    global df_hist
    global tidy_stats_jhop
    global df_jhopkins

    data_hist_json = API.historical()
    df_hist = pd.read_json(data_hist_json)
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
    'text': '#7FDBFF'
}

graph_style = {
            'legend': { 'x': 0, 'y': 1},
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {'color': colors['text']}
            }

app.layout = \
dbc.Container(
    html.Div(
        children = [
        html.Div(
            children=[
            html.H1(children='COVID-19',
                style={
                        'textAlign': 'center'
                    }),

            html.Div(children=
                html.H3('A presentation of data related to COVID-19.'),
            style={
                'textAlign': 'center'
                    }),
            
            html.Div(children = [
                html.P('\nTotal amount of Cases: {}'.format(count_sum_of_nested_dicts(df_jhopkins, 'stats', 'confirmed')), className ="text-warning"),
                html.P('Total amount of Deaths: {}'.format(count_sum_of_nested_dicts(df_jhopkins, 'stats', 'deaths')), className ="text-danger"),
                html.P('Total amount of Recovered cases: {}'.format(count_sum_of_nested_dicts(df_jhopkins, 'stats', 'recovered')), className ="text-success"),
                html.P('Last updated: {}'.format(max(df_jhopkins['updatedAt']))),
            ],
            style = { 'testAlign': 'center'}
            ),
################################################## BAR-GRAPH            
            html.Div(children= [
                dcc.Graph(
                    id='hist-tot-cases-by-country',
                    figure=px_plot_hist_jhop(tidy_stats_jhop).update_layout(graph_style)
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
                    id='log-trend',
                    figure= log_trend_all(df_hist, 25).update_layout(graph_style)
                ),
            ]),
##################################################### LINE-GRAPHS WITH DROPDOWN MENU
                html.Div(children=[
                    
                    html.Div(children = [
                            dcc.Dropdown(
                                id="drop",
                                options=[{'label': i, 'value': i } \
                                        for i in df_hist.loc[:, 'country'].unique()],
                                        value = 'Canada ontario',
                                        style=dict(
                                            width='40%',
                                            display='inline-block',
                                            verticalAlign="middle",
                                            color= colors['text'],
                                            bgcolor = colors['background']
                                        )
                        )
                    ]),

                    html.Div(children = [
                        dcc.Graph(
                            id='px-line-plot',
                            figure= px_line_plot(df_hist, 'Canada ontario').update_layout(graph_style),     
                        ),
                    ],
                    style={'width': '50%', 'display': 'inline-block'}
                    ),

                    html.Div(children= [
                            dcc.Graph(
                                id='px-line-plot-ratio',
                                figure= px_line_plot_ratio(df_hist, 'Canada ontario').update_layout(graph_style)
                            )
                    ],
                    style={'width': '50%', 'float': 'right', 'display': 'inline-block'}
                    ),
                ]),                       

            html.Div(children = [

                # dcc.Graph(
                #     id='map-plot',
                #     figure = map_plot(df_jhopkins)
                # )
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
# Run the server
if __name__ == "__main__":
    app.run_server(debug=False)

