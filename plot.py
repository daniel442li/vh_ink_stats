import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import requests
import json

url = "https://f4m3oqg1tg.execute-api.us-west-1.amazonaws.com/default/getStats"

response = requests.request("GET", url)

links = []
hits = []

for link in json.loads(response.text):
    links.append(link['path'])
    hits.append(link['hits'])



# Initialise the app
app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Link": links,
    "Clicks": hits,
})
fig = px.bar(df, x="Link", y="Clicks", barmode="group", template='plotly_dark').update_layout(
                                   {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                    'paper_bgcolor': 'rgba(0, 0, 0, 0)'})

# Define the app
app.layout = html.Div()

app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                  html.Div(className='four columns div-user-controls', children=[
                                            html.H2('Dashboard - vh.ink hit statistics'),
                                            html.P('''Visualising time series with Plotly - Dash'''),
                                            html.P('''Pick type of chart from the dropdown below.''')
                                  ]),  # Define the left element
                                  html.Div(className='eight columns div-for-charts bg-grey', children=[
                                    dcc.Graph(
                                        id='timeseries',
                                        config={'displayModeBar': False},
                                        figure=fig
                                    )                            
                                  ])  # Define the right element
                                  ])
                                  
                                ])




# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)