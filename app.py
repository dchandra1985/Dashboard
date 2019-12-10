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

colors = {
    'background': '#E6E7E8',
    'text': '#7FDBFF'
}

app.layout = html.Div(id='app-content', children=[

    html.Div(id='header-box', children=[

        html.Div(id='header-contents', children=[

            html.Div(className='banner', children=[

                html.Img(id="Left_Header_Image",
                         src="/assets/left.jpeg",
                         style={'float': 'left',
                                'margin-left': '0'}),

                html.Img(id="Right_Header_Image",
                         src="/assets/right.jpeg",
                         style={'float': 'right',
                                'margin-right': '0'}),

                html.H1(children="Global Emissions Analysis Dashboard",
                        style={'textAlign': 'center',
                               'padding': '1.5%',
                               'font-size': 'calc(1em + 1vw)'}),

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

        html.Br(),

        html.Div(id='interactive', children=[

            # Dropdown

            dcc.Dropdown(
                id="Get_Continent",
                options=[{'label': i, 'value': i} for i in conty
                         ],
                searchable=False,
                placeholder="Select Continents for Analysis",
                multi=True
            ),

        ], className='four columns'),

        # Range Slider

        html.Div([

            html.Br(),

            html.Label("Select number of years"),

            dcc.RangeSlider(
                id="Get_Year",
                min=min(year),
                max=max(year),
                step=5,
                value=[min(year), max(year)],
                marks={i: i for i in range(min(year), max(year) + 1, 5)},
                allowCross=False
            ),

        ], className='four columns'),

        # Dropdown

        html.Div([

            html.Br(),

            html.Label("X label"),

            dcc.Dropdown(
                id="Get_Xaxis",
                options=[{'label': i, 'value': i} for i in features
                         ],
                searchable=False,
                placeholder="Select a feature for Analysis"
            ),

        ], className='four columns'),

        # Dropdown

        html.Div([

            html.Br(),

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

    html.Div(children="© 2019-2020 Dinesh Chandrasekaran. All Rights Reserved.",
             style={"position": "relative",
                    "bottom": "-10px",
                    "left": "8px",
                    'font-size': 'calc(0.5em + 0.25vw)'})

])


@app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input('Submit-Button', 'n_clicks')],
    [State('Get_Xaxis', 'value'),
     State('Get_yaxis', 'value'),
     State('Get_Continent', 'value'),
     State('Get_Year', 'value')
     ]
)
def update_graph(n_clicks, X, y, cont, year_range):
    if n_clicks is None:  # users would rather write `if n_clicks == 0`
        return ''
    else:

        filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

        traces = []
        for i in cont:
            df_by_continent = filtered_df[filtered_df['Geography'] == i]
            traces.append(dict(
                x=df_by_continent[X],
                y=df_by_continent[y],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ))

        return {
            'data': traces,
            'layout': dict(
                title='{} and {} (barrels per day)'.format(X, y),
                xaxis={'title': X},
                yaxis={'title': y},
                plot_bgcolor=colors['background'],
                showlegend=True,
                # 'paper_bgcolor': colors['background'],
                hovermode='closest'
            )
        }


if __name__ == "__main__":
    app.run_server(debug=False)
