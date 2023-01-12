from dash import Dash, dcc, Output, Input
import pandas as pd
import plotly.express as px
from dash import html
import plotly.graph_objs as go
neighbourhood_groups = ['Manhattan', 'Brooklyn', 'Queens', 'Staten Island', 'Bronx']

df = pd.read_csv("cleaned_data_full.csv")
subway_df = pd.read_csv("subwaystations.csv")
app = Dash(__name__)

app.layout = html.Div([
    dcc.Checklist(id = 'neighbourhoodgroup_name',
                  options = neighbourhood_groups,
                  value = neighbourhood_groups),
    dcc.RangeSlider(0, 1200, value=[0, 1200], id='price_rangeslider'),

    dcc.Graph(id='graph')
])
@app.callback(Output('graph', 'figure'),
              [Input('neighbourhoodgroup_name', 'value'), Input('price_rangeslider','value')]
              )

def update_figure(selected_neighbourhoodgroups, price_range):
    df_filtered_neighbourhood = df[(df['neighbourhood group'].isin(selected_neighbourhoodgroups))]
    df_filtered_price = df_filtered_neighbourhood.loc[(df_filtered_neighbourhood['testprice'] >= price_range[0]) & (df['testprice'] <= price_range[1])]
    df_shown = df_filtered_price

    graph = px.scatter_mapbox(df_shown, lat="lat", lon="long", hover_name="NAME", hover_data=["testprice"],
                            color_discrete_sequence=["dodgerblue"], zoom=3, height=700)
    graph.update_layout(mapbox_style="carto-positron")
    graph.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    graph.update_mapboxes(bounds=dict(east = -73.163492 , north = 40.985341, south = 40.443028, west = -74.738340))
    graph.update_layout(uirevision = 'foo') #turn off if graph is shifting a lot with updates

    #trace_subway = go.Scattermapbox(subway_df,
                                   # lat = 'Station Latitude',
                                   # lon= 'Station Longitude',
                                   # hover_name= 'Station Name',
                                   # color='red',
                                  #  )
    #graph.add_trace(trace_subway)
    return graph

if __name__ == '__main__':
    app.run_server(debug=False)