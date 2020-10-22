import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State

# Load data
df = pd.read_pickle("all_tickers_last_decade_features.pkl")

# call Dash object/app
app = dash.Dash()

# layout = html to be shown
app.layout = html.Div([

    html.H1('Stocks'),
    html.Label('Elegir especie:'),

    # dropdown with ID 
    dcc.Dropdown(id='ticker_dropdown', 
        # llamo a un diccionario de tickers
        options=[{'label': item, 'value': item} for item in df['Ticker'].unique()],
        # puedo seleccionar más de un ticker
        multi=True, 
        value=[df['Ticker'].sort_values()[0]]),
    
    html.Label('Gráfico'),
    html.Div(
        # dcc.Graph doesn't receive 'figure' as argumento since is pass with the callback function
        dcc.Graph(id='stock_chart'))
    ])

# get value from dropdown and draw it on the figure of the stock chart
@app.callback(dash.dependencies.Output('stock_chart','figure'),
            [dash.dependencies.Input('ticker_dropdown','value')])
def update_figure(selected_tickers):
    "keep the figure (id=stock_chart) updated with the human selection (input=ticker_dropdown)"

    # empty list to be filled with the scatter of each ticker
    data = []

    # draw a scatter for the selected ticker
    for ticker in selected_tickers:
        data.append(go.Scatter(x=df[df['Ticker'] == ticker].index,
                                 y=df[df['Ticker'] == ticker]['Close'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=ticker,
                                 textposition='bottom center'))

    return {'data': data}

if __name__ == '__main__':
    app.run_server(debug=True)