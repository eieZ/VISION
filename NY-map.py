from dash import Dash, dcc, Output, Input, html
import plotly.io as pio
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import dash

neighbourhood_groups = ['Manhattan', 'Brooklyn', 'Queens', 'Staten Island', 'Bronx']
clsCode = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
df = pd.read_csv("datasets/superclean.csv")
df['Neighbourhood Group'] = df['neighbourhood group']
del df['neighbourhood group']

pio.templates.default = 'seaborn'
app = Dash(__name__)

app.layout = html.Div([
    #title
    html.Div([html.H1('JBI100 Dashboard', style={'textAlign': 'center'})]),
    #first row
    html.Div(children=[
        #first row first column
        html.Div(children=[
            html.H2('Neighbourhood Selection:'),
            html.Div(dcc.Dropdown(
                id='neighbourhoodgroup_name',
                options=neighbourhood_groups.copy(),
                multi=True,
                placeholder="Select Neighbourhoods:",
                value=neighbourhood_groups,
                ), style=dict(width='98%', textAlign = 'center', )),

            html.H2('Price Range:'),
            html.Div(dcc.RangeSlider(
                0, 
                1200, 
                value=[0, 1200], 
                id='price_rangeslider', 
                ), style=dict(width='100%')),
        ],style=dict(width = '45%',display = 'inline-block')),
            #first row second column
        html.Div(children=[
            html.Div(children= [
                html.H2('Verification Status:', style=dict(width='20%', display='inline-block')),
                html.H2('Booking Status :',style=dict(width='20%', display='inline-block')),
                html.H2('Room type:' , style=dict(width='20%', display='inline-block')),
                html.H2('Cancelation Policy:',style=dict(width='20%', display='inline-block')),
                html.H2('Rating Range:', style= dict(width='20%', display='inline-block'))
            ]),
            html.Div(children=[
                html.Div(dcc.Dropdown(
                    id='verification-status',
                    options=['verified', 'unconfirmed', 'All'],
                    placeholder='Verification Status:',
                    ),style= dict(width= '20%', display= 'inline-block')),
                html.Div(
                    dcc.Dropdown(
                        id='insta-bookable',
                        options= ['Yes', 'No', 'All'],
                        placeholder='Display Instantly Bookable',
                        ),style=dict(width= '20%', display= 'inline-block')),
                    html.Div(
                        dcc.Dropdown(
                    id='room-type',
                    options=['Private room', 'Entire home/apt', 'Shared room', 'Hotel room', 'All'],
                    placeholder='Room Type:',
                    value='All'
                    ),style= dict(width= '20%', display= 'inline-block')),
                    html.Div(dcc.Dropdown(
                    id='cancelation-policy',
                    options=['strict', 'moderate', 'flexible', 'All'],
                    placeholder='Cancellation Policy:',
                    value='All'
                    ),style= dict(width= '20%', display= 'inline-block')),
                    html.Div(dcc.RangeSlider(
                        1,
                        5,
                        id= 'rating-range',
                        value=[1,5]
                        ),style=dict(width= '20%', display= 'inline-block'))

                    ]),

            html.H2('Distance To Restauration:'),
            html.Div(dcc.RangeSlider(
                0, 
                2700, 
                value=[0, 2700], 
                id='bar_distance_rangeslider'
                ), style=dict(width='100%')
            )
        ], style=dict(width='45%', display= 'inline-block'))
        ]),
        html.Div(dcc.Graph(id='graph') ,style=dict(width = '50%', display = 'inline-block')),

        html.Div(dcc.Graph(id='bar-plot', figure={}), style=dict(width = '45%', display = 'inline-block') ),

        html.Div(dcc.Graph(id='violin-plot', figure={}), style=dict(width= '100%'))

    

])

    # html.Label('Neighbourhood Selection:'),
    # dcc.Dropdown(id='neighbourhoodgroup_name', options=neighbourhood_groups.copy(), multi=True, placeholder="Select Neighbourhoods:", value=neighbourhood_groups),
    # html.P('Price Range:'),
    # dcc.RangeSlider(0, 1200, value=[0, 1200], id='price_rangeslider'),

    # html.P('Distance To Bar:'),
    # dcc.RangeSlider(0, 2700, value=[0, 2700], id='bar_distance_rangeslider'),

    # html.P("Geographical Distribution Of AirBnBs In New York City"),
    # dcc.Graph(id='graph'),
    # dcc.Graph(id='violin-plot', figure={}),
    # dcc.Graph(id='bar-plot', figure={}),


#this part is for the map
@app.callback(
    Output('graph', 'figure'),
    Input('neighbourhoodgroup_name', 'value'),
    Input('price_rangeslider','value'),
    Input('bar_distance_rangeslider','value'),
    Input('verification-status', 'value'),
    Input('insta-bookable', 'value'),
    Input('room-type', 'value'),
    Input('cancelation-policy', 'value'),
    Input('rating-range', 'value'),
)


def update_figure_1(selected_neighbourhoodgroups, price_range, bar_distance, verif, book, room_type, cancel_pol, rating_range):
    # print(f'{verif}')
    # print(f'{book}')
    

    localDf = df.copy().sort_values(by=['Neighbourhood Group'])


    if verif == 'verified':
        localDf = localDf[localDf['host_identity_verified']==True]
    elif verif == 'unconfirmed':
        localDf = localDf[localDf['host_identity_verified']==False]
    
    
    if book == 'Yes':
        localDf = localDf[localDf['instant_bookable']==True]
    elif book == 'No':
        localDf = localDf[localDf['instant_bookable']==False]
    
    if room_type != 'All':
        localDf = localDf[pd.get_dummies(localDf['room type'])[room_type]==1]
    
    if cancel_pol != 'All':
        localDf = localDf[pd.get_dummies(localDf['cancellation_policy'])[cancel_pol]==1]

    localDf = localDf[(localDf['review rate number']>= rating_range[0]) & (localDf['review rate number']<= rating_range[1])]



    

    df_filtered_neighbourhood = localDf[(localDf['Neighbourhood Group'].isin(selected_neighbourhoodgroups))]
    df_filtered_price = df_filtered_neighbourhood.loc[(df_filtered_neighbourhood['price'] >= price_range[0]) & (df_filtered_neighbourhood['price'] <= price_range[1])]
    df_filtered_bar_distance = df_filtered_price.loc[(df_filtered_price['distance_to_closest_bar_m'] >= bar_distance[0]) & (df_filtered_price['distance_to_closest_bar_m'] <= bar_distance[1])]
    df_shown = df_filtered_bar_distance


    graph = px.scatter_mapbox(
        df_shown, 
        lat="lat", 
        lon="long", 
        hover_name="NAME", 
        hover_data=["price"],
        zoom=3,
        height=700,
        color= 'Neighbourhood Group', 
        color_discrete_sequence= clsCode[:len(selected_neighbourhoodgroups)],
        category_orders={'Neighbourhood Group': selected_neighbourhoodgroups})


    graph.update_layout(mapbox_style="carto-positron")
    graph.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    graph.update_mapboxes(bounds=dict(east = -73.163492 , north = 40.985341, south = 40.443028, west = -74.738340))
    graph.update_layout(uirevision = 'foo') #turn off if graph is shifting a lot with updates
    graph.update_layout(legend= dict(x = 0))
    return graph
    # else:
    #     raise dash.exceptions.PreventUpdate()

#part for the violin plot

@app.callback(
    Output('violin-plot', 'figure'),
    Input('neighbourhoodgroup_name', 'value'),
    Input('price_rangeslider','value'),
    Input('bar_distance_rangeslider','value'),
    Input('verification-status', 'value'),
    Input('insta-bookable', 'value'),
    Input('room-type', 'value'),
    Input('cancelation-policy', 'value'),
    Input('rating-range', 'value'),
)

def update_figure_2(selected_neighbourhoodgroups, price_range, bar_distance, verif, book, room_type, cancel_pol, rating_range):
    localDf = df.copy().sort_values(by=['Neighbourhood Group'])

    if verif == 'verified':
        localDf = localDf[localDf['host_identity_verified']==True]
    elif verif == 'unconfirmed':
        localDf = localDf[localDf['host_identity_verified']==False]
    
    
    if book == 'Yes':
        localDf = localDf[localDf['instant_bookable']==True]
    elif book == 'No':
        localDf = localDf[localDf['instant_bookable']==False]
    

    if room_type != 'All':
        localDf = localDf[pd.get_dummies(localDf['room type'])[room_type]==1]

    if cancel_pol != 'All':
        localDf = localDf[pd.get_dummies(localDf['cancellation_policy'])[cancel_pol]==1]
    
    localDf = localDf[(localDf['review rate number']>= rating_range[0]) & (localDf['review rate number']<= rating_range[1])]


    df_filtered_neighbourhood = localDf[(localDf['Neighbourhood Group'].isin(selected_neighbourhoodgroups))]
    df_filtered_price = df_filtered_neighbourhood.loc[(df_filtered_neighbourhood['price'] >= price_range[0]) & (df['price'] <= price_range[1])]
    df_filtered_bar_distance = df_filtered_price.loc[(df_filtered_price['distance_to_closest_bar_m'] >= bar_distance[0]) & (df_filtered_price['distance_to_closest_bar_m'] <= bar_distance[1])]
    df_shown = df_filtered_bar_distance
    df_shown['Price'] = df_shown['price']

    violin_plot = px.violin(
        df_shown, 
        y='Price', 
        x='Neighbourhood Group',
        box=True, 
        color = 'Neighbourhood Group', 
        color_discrete_sequence= clsCode[:len(selected_neighbourhoodgroups)],
        title= "Price Distribution For Selected Criteria By Neighbourhoods", 
        category_orders={'Neighbourhood Group': selected_neighbourhoodgroups})
    # violin_plot.update_yaxes('Price')
    violin_plot.update_layout(
        showlegend=False
    )
    return violin_plot


# for the bar chart

@app.callback(
    Output('bar-plot', 'figure'),
    Input('neighbourhoodgroup_name', 'value'),
    Input('price_rangeslider','value'),
    Input('bar_distance_rangeslider','value'),
    Input('verification-status', 'value'),
    Input('insta-bookable', 'value'),
    Input('room-type', 'value'),
    Input('cancelation-policy', 'value'),
    Input('rating-range', 'value'),
)

def update_figure_3(selected_neighbourhoodgroups, price_range, bar_distance, verif, book, room_type, cancel_pol, rating_range):
    # selected_neighbourhoodgroups = selected_neighbourhoodgroups.sort()
    localDf = df.copy().sort_values(by=['Neighbourhood Group'])


    if verif == 'verified':
        localDf = localDf[localDf['host_identity_verified']==True]
    elif verif == 'unconfirmed':
        localDf = localDf[localDf['host_identity_verified']==False]
    
    
    if book == 'Yes':
        localDf = localDf[localDf['instant_bookable']==True]
    elif book == 'No':
        localDf = localDf[localDf['instant_bookable']==False]

    if room_type != 'All':
        localDf = localDf[pd.get_dummies(localDf['room type'])[room_type]==1]
    
    if cancel_pol != 'All':
        localDf = localDf[pd.get_dummies(localDf['cancellation_policy'])[cancel_pol]==1]

    localDf = localDf[(localDf['review rate number']>= rating_range[0]) & (localDf['review rate number']<= rating_range[1])]

    df_filtered_neighbourhood = localDf[(localDf['Neighbourhood Group'].isin(selected_neighbourhoodgroups))]
    df_filtered_price = df_filtered_neighbourhood.loc[(df_filtered_neighbourhood['price'] >= price_range[0]) & (df['price'] <= price_range[1])]
    df_filtered_bar_distance = df_filtered_price.loc[(df_filtered_price['distance_to_closest_bar_m'] >= bar_distance[0]) & (df_filtered_price['distance_to_closest_bar_m'] <= bar_distance[1])]
    df_shown = df_filtered_bar_distance

    ddF = df_shown[['Neighbourhood Group', 'price', 'review rate number']].reset_index()
    del ddF['index']
    rats = pd.DataFrame()
    ls = []
    for name in selected_neighbourhoodgroups:
        ls.append(ddF[ddF['Neighbourhood Group'] == name]['review rate number'].sum() / len(
            ddF[ddF['Neighbourhood Group'] == name]))
    rats['average rating'] = ls
    rats['Neighbourhood Group'] = selected_neighbourhoodgroups
    bar = px.bar(
        rats, 
        x='Neighbourhood Group', 
        y='average rating', 
        color = 'Neighbourhood Group',
        color_discrete_sequence= clsCode[:len(selected_neighbourhoodgroups)], 
        title='Average AirBnB Rating For Given Criteria By Neighbourhood', 
        category_orders={'Neighbourhood Group': selected_neighbourhoodgroups})

    bar.update_xaxes(title_text='Neighbourhood')
    bar.update_yaxes(title_text='Mean Rating')
    bar.update_layout(
    height = 700,
    showlegend= False,
    yaxis=dict(
    range=[0, 5]
    ))


    return bar


if __name__ == '__main__':
    app.run_server(debug=False)