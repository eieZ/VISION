from dash import Dash, dcc, html, Output, Input
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from vioPlot import getData

nbhdLs = ['Manhattan', 'Brooklyn', 'Queens', 'Staten Island', 'Bronx']

app = Dash(__name__)

data = getData()

app.layout = html.Div([
    html.H1("Ratings Against Price"),
    dcc.Dropdown(id ='scatt-dd', options=nbhdLs.copy(), multi=True, placeholder= "Select Neighbourhoods:"),
    dcc.Graph(id='scatter-plot'),
    html.P("Filter by Rating:"),
    dcc.RangeSlider(id='range-slider',
        min=0,
        max=5,
        step=0.1,
        marks={0:"0", 5:"5"},
        value=[0, 5]
        ),
    ])




@app.callback(
        Output('scatter-plot', 'figure'),
        [Input('scatt-dd', 'value'), 
            # Input('range-slider', 'value')
            ]
        )
def update_scatter_plot(scatter_select):
    # low, high =
    scatterFrame = pd.DataFrame()
    for neighbourhood in scatter_select:
        scatterFrame = pd.concat(
                [scatterFrame,
                    data[data["neighbourhood group"] == neighbourhood]
                    ]
                )
    scatter = px.scatter(scatterFrame,
            y = "rating",
            x = "price",
            color = "neighborhood group")
    return scatter

if __name__ == "__main__":
    app.run_server(debug=True)