import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction

from graph_functions import * 
from cleaning_functions import *
from API.call_functions import *

# Data Imports 

API = calls()

data_hist_json = API.historical()

df_hist = pd.read_json(data_hist_json)

df_hist = tidy_historical(df_hist)


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.layout = html.Div(children=[
    html.H1(children='COVID-19',
        style={
                'textAlign': 'center'
            }),

    html.Div(children='''
        A presentation of data related to COVID-19.
    ''',
    style={
           'textAlign': 'center'
            }),

    html.Div(children=(
   
    dcc.Graph(
        id='px-line-plot',
        figure= px_line_plot(df_hist, 'canada')
        
    ),

    dcc.Dropdown(
        id="drop",
        options=[{'label': i, 'value': i } \
                for i in df_hist.loc[:, 'country'].unique()],
                 value = 'canada ontario'
    )
    )
    ),

    html.Div(children= [
        dcc.Graph(
            id='hist-tot-cases-by-country',
            figure=px_plot_hist(df_hist)
        )
    ])
])

@app.callback(
    Output(component_id='px-line-plot', component_property='figure'),
    [Input(component_id='drop', component_property='value')]
)
def update_output_div(input_value):
    return px_line_plot(df_hist, input_value)
# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)