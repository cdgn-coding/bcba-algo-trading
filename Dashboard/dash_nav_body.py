import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State

# Load data
df = pd.read_pickle("all_tickers_last_decade_features.pkl")

LOGO = "/assets/bullish_logo.png"

# call Dash object/app with bootstrap
app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# make a reuseable navitem for the different examples
nav_item = dbc.NavItem(dbc.NavLink("Link", href="https://www.clubaindependiente.com.ar/"))

# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Entry 1"),
        dbc.DropdownMenuItem("Entry 2"),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Entry 3"),
    ],
    nav=True,
    in_navbar=True,
    label="Menu",
)

NAVBAR = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("DASHBOARD", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [nav_item, dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-5",
)

STOCKS_CHART = [
    dbc.CardHeader(html.H5("Stocks' Close Prices")),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                    html.P("Choose Tickers"),
                    # dropdown with ID 
                    dcc.Dropdown(id='ticker_dropdown', 
                        # pass a list of ticker dicts
                        options=[{'label': item, 'value': item} for item in df['Ticker'].unique()],
                        # selection of multiple tickers possible
                        multi=True, 
                        value=[df['Ticker'].sort_values()[0]]
                    )
                ],
            ),
        ]),
        dbc.Row(
            dbc.Col( dcc.Graph(id='stock_chart'))
            )
    ])
]

TABLE = dbc.Jumbotron([
        html.H4(children="Table", className="display-5"),
        html.Hr(className="my-2"),
        html.Label("Price at close", className="lead", style={'padding-bottom':'10%'}),
            dash_table.DataTable(id='table',
                columns=[
                    {"name": i, "id": i} for i in df.loc[:,['Adj Close','Ticker']].columns],
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold',
                    'textAlign': 'center'
                },
                style_cell={'fontSize':12, 'textAlign': 'left'},
                page_current=0,
                page_size=10,
                page_action='custom',
            ),

    ])

BODY = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(STOCKS_CHART), md=8),
                dbc.Col(TABLE, md=4, align="center")
            ],
            style={"marginTop": 30},
        ),
    ],
)

# layout = html to be shown
app.layout = html.Div([NAVBAR,BODY])

# we use a callback to toggle the collapse on small screens
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
# the same function (toggle_navbar_collapse) is used in all three callbacks
app.callback(
    Output(f"navbar-collapse", "is_open"),
    [Input(f"navbar-toggler", "n_clicks")],
    [State(f"navbar-collapse", "is_open")],
)(toggle_navbar_collapse)

# get value from dropdown and draw it on the figure of the stock chart
@app.callback(Output('stock_chart','figure'),
            [Input('ticker_dropdown','value')])
def update_figure(selected_tickers):
    "keep the figure (id=stock_chart) updated with the human selection (input=ticker_dropdown)"

    # empty list to be filled with the scatter/candlestick of each ticker
    data=[]

    # two iterations: a list of scatter objects before a list of candlestick object
    for ticker in selected_tickers:
        data.append(go.Scatter(x=df[df['Ticker'] == ticker].index,
                                 y=df[df['Ticker'] == ticker]['Close'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=ticker,
                                 textposition='bottom center'))
        
    for ticker in selected_tickers:
        data.append(go.Candlestick(x=df[df['Ticker'] == ticker].index,
                            open=df[df['Ticker'] == ticker]['Open'],
                            high=df[df['Ticker'] == ticker]['High'],
                            low=df[df['Ticker'] == ticker]['Low'],
                            close=df[df['Ticker'] == ticker]['Close'],
                            visible=False,
                            showlegend=False))
    
    updatemenus = list([
        dict(
            buttons=list([
                dict(
                    args=[{'visible': [True, False]}],
                    label='Line',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, True]}],
                    label='Candle',
                    method='update'
                ),
            ]),
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=0,
            xanchor='left',
            y=1.05,
            yanchor='top'
        ),
    ])

    layout = dict(
        updatemenus=updatemenus,
        autosize=False,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                         label='YTD',
                         step='year',
                         stepmode='todate'),
                    dict(count=1,
                         label='1y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date'
        )
    )

    # data must be a list of objects and not a list of lists
    return {
        "data": data,
        "layout": layout
    }

# gets the value from the dropdown and the pagination
@app.callback(Output('table', 'data'),
            [Input('ticker_dropdown', "value"),
            Input('table', "page_current"),
            Input('table', "page_size")])
def update_table(selected_tickers,page_current,page_size):
    "cuts the dataframe with the chosen tickers and showa only the rows which fits in the pagination"
    data = df.loc[df['Ticker'].isin(selected_tickers),['Adj Close','Ticker']]
    return data.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)