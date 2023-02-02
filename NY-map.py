from dash import Dash, dcc, Output, Input
import pandas as pd
import plotly.express as px
from dash import html
import plotly.graph_objs as go
neighbourhood_groups = ['Manhattan', 'Brooklyn', 'Queens', 'Staten Island', 'Bronx']

df = pd.read_csv("Cleaned_data_bar_distance.csv")

app = Dash(__name__)

app.layout = html.Div([
    #dcc.Checklist(id = 'neighbourhoodgroup_name', to be changed with dropdown
                 #options = neighbourhood_groups,
                 # value = neighbourhood_groups),
    html.H1('Violin Plot With drop down in Dash'),
    dcc.Dropdown(id='neighbourhoodgroup_name', options=neighbourhood_groups.copy(), multi=True,
                 placeholder="Select Neighbourhoods:", value=neighbourhood_groups),
    dcc.RangeSlider(0, 1200, value=[0, 1200], id='price_rangeslider'),
    dcc.RangeSlider(0, 2700, value=[0, 2700], id='bar_distance_rangeslider'),
    dcc.Graph(id='graph'),
    dcc.Graph(id='violin-plot', figure={}),
    dcc.Graph(id='bar-plot', figure={}),
])
#this part is for the map
@app.callback(
    Output('graph', 'figure'),
    Input('neighbourhoodgroup_name', 'value'),
    Input('price_rangeslider','value'),
    Input('bar_distance_rangeslider','value')
)


def update_figure_1(selected_neighbourhoodgroups, price_range, bar_distance):
    df_filtered_neighbourhood = df[(df['neighbourhood group'].isin(selected_neighbourhoodgroups))]
    df_filtered_price = df_filtered_neighbourhood.loc[(df_filtered_neighbourhood['testprice'] >= price_range[0]) & (df['testprice'] <= price_range[1])]
    df_filtered_bar_distance = df_filtered_price.loc[(df_filtered_price['distance_to_closest_bar_m'] >= bar_distance[0]) & (df_filtered_price['distance_to_closest_bar_m'] <= bar_distance[1])]
    df_shown = df_filtered_bar_distance


    graph = px.scatter_mapbox(df_shown, lat="lat", lon="long", hover_name="NAME", hover_data=["testprice"],
                            color_discrete_sequence=["dodgerblue"], zoom=3, height=700, color = 'neighbourhood group')
    graph.update_layout(mapbox_style="carto-positron")
    graph.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    graph.update_mapboxes(bounds=dict(east = -73.163492 , north = 40.985341, south = 40.443028, west = -74.738340))
    graph.update_layout(uirevision = 'foo') #turn off if graph is shifting a lot with updates
    return graph

#part for the violin plot

@app.callback(
    Output('violin-plot', 'figure'),
    Input('neighbourhoodgroup_name', 'value'),
    Input('price_rangeslider','value'),
    Input('bar_distance_rangeslider','value')
)

def update_figure_2(selected_neighbourhoodgroups, price_range, bar_distance):

    df_filtered_neighbourhood = df[(df['neighbourhood group'].isin(selected_neighbourhoodgroups))]
    df_filtered_price = df_filtered_neighbourhood.loc[(df_filtered_neighbourhood['testprice'] >= price_range[0]) & (df['testprice'] <= price_range[1])]
    df_filtered_bar_distance = df_filtered_price.loc[(df_filtered_price['distance_to_closest_bar_m'] >= bar_distance[0]) & (df_filtered_price['distance_to_closest_bar_m'] <= bar_distance[1])]
    df_shown = df_filtered_bar_distance
    violin_plot = px.violin(df_shown, y='testprice', x='neighbourhood group', box=True, color = 'neighbourhood group')

    return violin_plot

# for the bar chart

@app.callback(
    Output('bar-plot', 'figure'),
    Input('neighbourhoodgroup_name', 'value'),
    Input('price_rangeslider','value'),
    Input('bar_distance_rangeslider','value')
)

def update_figure_3(selected_neighbourhoodgroups, price_range, bar_distance):

    df_filtered_neighbourhood = df[(df['neighbourhood group'].isin(selected_neighbourhoodgroups))]
    df_filtered_price = df_filtered_neighbourhood.loc[(df_filtered_neighbourhood['testprice'] >= price_range[0]) & (df['testprice'] <= price_range[1])]
    df_filtered_bar_distance = df_filtered_price.loc[(df_filtered_price['distance_to_closest_bar_m'] >= bar_distance[0]) & (df_filtered_price['distance_to_closest_bar_m'] <= bar_distance[1])]
    df_shown = df_filtered_bar_distance

    if len(selected_neighbourhoodgroups) > 0:

       # mn, max = price_range
        #local = data[(data['testprice'] > mn) & (data['testprice'] < max)]
        #dcp = local[local['neighbourhood group'].isin(valchosen)]

        ddF = df_shown[['neighbourhood group', 'testprice', 'review rate number']].reset_index()
        del ddF['index']
        rats = pd.DataFrame()
        ls = []
        for name in selected_neighbourhoodgroups:
            ls.append(ddF[ddF['neighbourhood group'] == name]['review rate number'].sum() / len(
                ddF[ddF['neighbourhood group'] == name]))
        rats['average rating'] = ls
        rats['nbhds'] = selected_neighbourhoodgroups
        bar = px.bar(rats, x='nbhds', y='average rating', color = 'nbhds')
        bar.update_layout(
        yaxis=dict(
        range=[0, 5]
        ))


    return bar


if __name__ == '__main__':
    app.run_server(debug=False)