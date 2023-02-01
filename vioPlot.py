from dash import Dash, dcc, html, Output, Input
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

app = Dash(__name__)

nbhdGrpls = ['Manhattan', 'Brooklyn', 'Queens', 'Staten Island', 'Bronx']

def getData():
    # This function imports the clean data and formats it for use
    data = pd.read_csv("datasets/clean.csv")
    del data['Unnamed: 0']
    data.head()
    return data


data= getData()

@app.callback(
    Output('violin-plot', 'figure'),
    [Input('neigh-dd', 'value')]
)

def update_violin_plot(neighbourhoods):
    filteredFinal = pd.DataFrame()
    for neighbourhood in neighbourhoods:
        filteredFinal = pd.concat([filteredFinal, data[data['neighbourhood group'] == neighbourhood]])
    violin = px.violin(filteredFinal, y='price', x='neighbourhood group', box=True)
    return violin

app.layout = html.Div([
    html.H1('Violin Plot With drop down in Dash'),
    dcc.Dropdown(id='neigh-dd', options=nbhdGrpls.copy(), multi=True, placeholder="Select Neighbourhoods:"),
    dcc.Graph(id='violin-plot', figure={})
])

if __name__ == "__main__":
    app.run_server(debug=True)

