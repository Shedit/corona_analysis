import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc

dbc.Container(
    dbc.Row([
        dbc.Card(
            dbc.CardBody(
                html.Div(children = [
                    dcc.Graph(
                        id='px-line-plot',
                        figure= px_line_plot(df_hist, 'Canada ontario').update_layout(graph_style),     
                    )]
                )            
            )
        ), 
        dbc.Card(
            dbc.CardBody(
                html.Div(children= [
                    dcc.Graph(
                        id='px-line-plot-ratio',
                        figure= px_line_plot_ratio(df_hist, 'Canada ontario').update_layout(graph_style)
                    )]
                ),
            )
        )
    ])
)



            html.Div(children= [
                    dcc.Graph(
                        id='px-line-plot-ratio',
                        figure= px_line_plot_ratio(df_hist, 'Canada ontario').update_layout(graph_style)
                    )],
            ),