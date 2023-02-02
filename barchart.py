from dash import Dash, dcc, html, Output, Input, State
import dash
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from vioPlot import getData
data = getData()
nbhdLs = ['Manhattan', 'Brooklyn', 'Queens', 'Staten Island', 'Bronx']
app = Dash(__name__)

app.layout= html.Div([
    dcc.Dropdown(
        id='mn-nbhd-rtng-nbhd',
        multi=True,
        options= nbhdLs.copy(),
        value=['Bronx']),
    html.Button(id='mn-nbhd-rtng-button', n_clicks=0, children="Show breakdown"),
    dcc.Graph(id='graph-output', figure={}),

    html.P("Select A Price Range:"),
    dcc.RangeSlider(id= 'mn-nbhd-rtng-price',
    min=0,
    max= 1200,
    step=20,
    marks={
        0:'0',
        100:'100',
        200:'200',
        300:'300',
        400:'400',
        500:'500',
        600:'600',
        700:'700',
        800:'800',
        900:'900',
        1000:'1000',
        1100:'1100',
        1200:'1200'
    },
    value= [0,400]
    )
])

@app.callback(
    Output(component_id='graph-output', component_property='figure'),
    [Input(component_id='mn-nbhd-rtng-button', component_property='n_clicks')],
    [State(component_id='mn-nbhd-rtng-nbhd', component_property='value'),
    State(component_id='mn-nbhd-rtng-price', component_property='value')
    ]

)
def barupdater(n, valchosen, ranger):
    if len(valchosen)>0:
        print(f'chosen user values:{valchosen}')
        print(type(valchosen))
        print(f'{n}')
        print(type(n))
        print(f'{ranger}')
        print(type(ranger))
        mn, max = ranger
        local = data[(data['price']> mn) &(data['price']<max)]
        dcp= local[local['neighbourhood group'].isin(valchosen)]
        ddF = dcp[['neighbourhood group', 'price', 'review rate number']].reset_index()
        del ddF['index']
        rats = pd.DataFrame()
        ls = []
        for name in valchosen:
            ls.append(ddF[ddF['neighbourhood group']==name]['review rate number'].sum() / len(ddF[ddF['neighbourhood group']==name]))
        rats['average rating'] = ls
        rats['nbhds']= valchosen
        bar = px.bar(rats, x = 'nbhds', y='average rating', color='nbhds')
        bar.update_yaxes(range = [0,5])
        return bar
    else:
        raise dash.exceptions.PreventUpdate()




if __name__ == '__main__':
    app.run_server(debug=True)
