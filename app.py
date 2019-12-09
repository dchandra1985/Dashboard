import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import random
import numpy as np
import plotly.graph_objs as go
import dash_daq as daq

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv("./data/petroleum.csv", header=0)

conty = df['Geography'].unique()

features = ["Import", "Export", "CO2_Emissions"]

year = df['Year'].unique()

data = {i for i in range(min(year), max(year))}

# tmp = df[df['Geography'] == 'Asia']



# Initialize the application

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(id='app-content', children=[

    html.Div(id='header-box', children=[

        html.Div(id='header-contents', children=[

            html.Div(className='banner', children=[

                html.Img(id="Left_Header_Image",
                         src="/assets/left.jpg",
                         style={'float': 'left'}),

                html.Img(id="Right_Header_Image",
                         src="/assets/right.jpg",
                         style={'float': 'right'}),

                html.Div(children="Global Emissions Analysis Dashboard",
                         className='six columns offset-by-two',
                         style={"textAlign": 'center', 'font-size': '2em', 'color': 'white'}),

                # html.Div(children="Import and of Petroleum",
                #     className='six columns offset-by-two',
                #     style={"textAlign": 'center', 'font-size': '1em', 'color' : 'white'}),

            ]),

        ], className='twelve columns'),

    ], className='row'),

    #  Next Row

    html.Div(id='plot', children=[

        html.Div(children=[
            dcc.Graph(
                id='graph'
            )
        ], className='eight columns'),

        html.Div(id='interactive', children=[

            # Dropdown

            dcc.Dropdown(
                id="Get_Continent",
                options=[{'label': i, 'value': i} for i in conty
                         ],
                searchable=False,
                placeholder="Select a Continent for Analysis"
            ),

        ], className='four columns'),

        html.Br(),
        html.Br(),

        # Dropdown

        html.Div([

            html.Label("X label"),

            dcc.Dropdown(
                id="Get_Xaxis",
                options=[{'label': i, 'value': i} for i in features
                         ],
                searchable=False,
                placeholder="Select a feature for Analysis"
            ),

        ], className='four columns'),

        html.Br(),
        html.Br(),
        html.Br(),

        # Dropdown

        html.Div([

            html.Label("y label"),

            dcc.Dropdown(
                id="Get_yaxis",
                options=[{'label': i, 'value': i} for i in features
                         ],
                searchable=False,
                placeholder="Select a feature for Analysis"
            ),

            html.Br(),


            html.Button('Submit',
                        id="Submit-Button",
                        n_clicks=0,
                        ),

            html.Div(id='output')

        ], className='four columns'),

    ], className="row"),

])


@app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input('Submit-Button', 'n_clicks')],
    [State('Get_Xaxis', 'value'),
     State('Get_yaxis', 'value'),
     State('Get_Continent', 'value')]
)
def update_graph(n_clicks, X, y, cont):

    if n_clicks is None:  # users would rather write `if n_clicks == 0`
        return ''
    else:

        df1 = df[df['Geography'] == cont]

        return {
            'data': [
                {'x': df1[X],
                 'y': df1[y],
                 'name': '{} and {}'.format(X,y),
                 'mode': 'markers',
                 'marker': {'size': 12},
                 },
            ],
            'layout': {
                'title' : 'Petroleum {} and {} Analysis in {} (Barrel)'.format(X,y,cont),
                'xaxis' : {'title' : X},
                'yaxis': {'title': y},
                'showlegend':True,
                'hovermode' : 'closest'
            }
        }


if __name__ == "__main__":
    app.run_server(debug=False)
