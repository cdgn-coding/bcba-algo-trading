# Import required libraries
import dash
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import dash_table


LOGO = "/assets/logo-dh-blanco.png"
GIT_LOGO = "/assets/github.png"

df = pd.read_csv("/home/thomas/Descargas/all_tickers_last_decade_features_usd.csv")

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.JOURNAL]
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

page_2_layout = html.Div([

    dcc.Store(id="aggregate_data"),

    html.Div(id="output-clientside"),
    html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.H3(
                                "Stock Prices Forecasting",
                                style={"margin-bottom": "0px"},
                            ),
                            html.H5(
                                "Algorithmic Trading Overview", style={"margin-top": "0px"}
                            ),
                        ]
                    )
                ],
                className="one-half column",
                id="title",
            )
        ],
        id="header",
        className="row flex-display",
        style={"margin-bottom": "25px"},
    ),

    dcc.Link('Go back to home', href='/page-1'),

    html.Div(
            [
            html.Div(
                [
                    html.P(
                        "Tickers:",
                        className="control_label",
                    ),
                    dcc.Dropdown(
                        options=[{'label': item, 'value': item} for item in df['Ticker'].unique()],
                        id='ticker_for_dropdown',
                        multi=False,
                        className="dcc_control",
                        value=df['Ticker'].sort_values()[0]
                    ),
                ],
                className="pretty_container four columns",
                id="cross-filter-options"
            ),
            # Bloques
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [html.P("Last Price"), html.H6(id="last_price")],
                                id="wells",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.P("Future Variation"), html.H6(id="var_for")],
                                id="gas",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.P("Price Forecast"), html.H6(id="price_for")],
                                id="oil",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.P("Strategy"), html.H6(id="strategy")],
                                id="water",
                                className="mini_container",
                            ),
                        ],
                        id="info-container",
                        className="row container-display",
                    ),
                    # grafico interno
                    html.Div(
                        dcc.Graph(id="stock_for_chart"),
                        id="countGraphContainer",
                        className="pretty_container",
                    ),
                ],
                id="right-column",
                className="eight columns",
            ),
        ],
        className="row flex-display main-content-container",
    )


])

nav_item = dbc.NavItem(dbc.NavLink("Link", href="#"))

page_2_link = dbc.NavItem(dbc.NavLink("Ver pronostico", href="/page-2"))

project_link = dbc.NavItem(dbc.NavLink("Ir al codigo del proyecto", href="https://github.com/cnexans/bcba-algo-trading", target="_blank"))

project_link_logo = html.A(
            html.Img(src=GIT_LOGO, style={ "height": "40px" }),
            href="https://github.com/cnexans/bcba-algo-trading",
            target="_blank",
            className="github-link"
        )

# dropdown_nav = dbc.DropdownMenu(
#     children=[
#         dbc.DropdownMenuItem("Ver recomendacion", href = "/page-2"),
#         dbc.DropdownMenuItem("Entry 2"),
#     ],
#     nav=True,
#     in_navbar=True,
#     label="Menu",
# )

# Create app layout
page_1_layout = html.Div(
    [
        # HEAD
        dcc.Store(id="aggregate_data"),

        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Stock Prices Forecasting",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Algorithmic Trading Overview", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),

html.Div(
         dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=LOGO, height="50px")),
                            ],
                            align="center",
                            no_gutters=True,
                        ),
                    ),
                    dbc.NavbarToggler(id="navbar-toggler"),
                    dbc.Collapse(
                        dbc.Nav(
                            [page_2_link, project_link_logo], className="ml-auto", navbar=True
                        ),
                        id="navbar-collapse",
                        navbar=True,
                    ),
                ]
            ),
            color="dark",
            dark=True,
            className="mb-5",
         ),
 ),

        # MAIN        
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            "Choose tickers",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            options=[{'label': item, 'value': item} for item in df['Ticker'].unique()],
                            id='ticker_dropdown',
                            multi=True,
                            className="dcc_control",
                            value=[df['Ticker'].sort_values()[0]]
                        ),
                        html.H6("Chart type", className="control_label"),
                        dcc.RadioItems(
                            id="graph_selector",
                            options=[
                                {"label": "Line ", "value": "line"},
                                {"label": "Candle", "value": "candle"},
                                {"label": "Bar", "value": "bar"},
                            ],
                            value="line",
                            labelStyle={"display": "inline-block","margin-right": "20px"},
                            className="dcc_control",
                        ),
                        html.H6("Prices", className="control_label"),
                        html.Div(
                                dash_table.DataTable(id='table',
                                columns=[
                                    {"name": i, "id": i} for i in df.loc[:,['Adj Close','Ticker']].columns],
                                style_header={
                                    'fontWeight': 'bold',
                                    'padding': '8px'
                                },
                                style_cell={
                                    'backgroundColor': '#f9f9f9',
                                    'fontSize':12, 
                                    'textAlign': 'center',
                                    'padding': '5px'},
                                style_as_list_view=True,
                                page_current=0,
                                page_size=7,
                                page_action='custom',
                            ),
                            style={'padding': '25px 80px 60px 20px','justify-content': 'center'},
                        )
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),

                # Bloques
                html.Div(
                    [
                        # grafico interno
                        html.Div([
                            html.H4("Prices at close", className="control_label"),
                            dcc.Graph(id="stock_chart")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
            style={"display": "flex", "flex-direction": "row"}
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-2':
        return page_2_layout
    else:
        return page_1_layout
    # You could also return a 404 "URL not found" page here

@app.callback([Output('last_price', 'children'),
            Output('var_for', 'children'),
            Output('price_for', 'children'),
            Output('strategy', 'children')],
            [Input('ticker_for_dropdown','value')])
def display_values(ticker):

    import joblib
    modelo = joblib.load('models/trained_model_Forward_Return_1m.joblib')
    ticker_history = df.loc[df['Ticker'] == ticker]
    prediction = modelo.predict(ticker_history)

    var = str(round(prediction[-1],2))
    price = round(df.loc[df['Ticker'] == ticker].iloc[-1,:]['Adj Close'],2)
    new_price = round(price * (1 + prediction[-1]),2)

    # modificar en base a futuras predicciones
    advise = 'Sell'
    if new_price > price:
        advise = 'Buy'

    print(price, var, new_price, advise)

    return price, var, new_price, advise

# get value from dropdown and draw it on the figure of the stock chart
@app.callback(Output('stock_for_chart','figure'),
            [Input('ticker_for_dropdown','value')])
def update_for_figure(ticker):
    "keep the figure (id=stock_chart) updated with the human selection (input=ticker_dropdown)"

    # empty list to be filled with the scatter/candlestick of each ticker
    figure = go.Scatter(x=df[df['Ticker'] == ticker].index,
                        y=df[df['Ticker'] == ticker]['Close'],
                        mode='lines')
    
    layout = dict(
            xaxis = dict(
            showgrid= False,
            zeroline= False,
            rangeslider=dict(
            visible=True
            ),
            type='date',
            rangeselector = dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                    ])
                )
            ),
            yaxis = {
            "showgrid": True,
            "zeroline": True,
            },
            margin=dict(l=30, r=30, b=0, t=40),
            hovermode="closest",
            plot_bgcolor="#F9F9F9",
            paper_bgcolor="#F9F9F9",
            legend=dict(font=dict(size=10),
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1)
            )
    
    # data must be a list of objects and not a list of lists
    return {"data": [figure], 'layout':layout}
















# get value from dropdown and draw it on the figure of the stock chart
@app.callback(Output('stock_chart','figure'),
            [Input('graph_selector','value'),
            Input('ticker_dropdown','value')])
def update_figure(chart_type, selected_tickers):
    "keep the figure (id=stock_chart) updated with the human selection (input=ticker_dropdown)"

    # empty list to be filled with the scatter/candlestick of each ticker
    data=[]

    # two iterations: a list of scatter objects before a list of candlestick object
    if chart_type == 'line':
        for ticker in selected_tickers:
            data.append(go.Scatter(x=df[df['Ticker'] == ticker].index,
                                    y=df[df['Ticker'] == ticker]['Close'],
                                    mode='lines',
                                    name=ticker,
                                    text=ticker,
                                    showlegend=True))
    elif chart_type == 'candle':       
        for ticker in selected_tickers:
            data.append(go.Candlestick(x=df[df['Ticker'] == ticker].index,
                                open=df[df['Ticker'] == ticker]['Open'],
                                high=df[df['Ticker'] == ticker]['High'],
                                low=df[df['Ticker'] == ticker]['Low'],
                                close=df[df['Ticker'] == ticker]['Close'],
                                name=ticker,
                                text=ticker,
                                showlegend=True))
    else:       
        for ticker in selected_tickers:
            data.append(go.Bar(x=df[df['Ticker'] == ticker].index,
                                y=df[df['Ticker'] == ticker]['Close'],
                                name=ticker,
                                text=ticker,
                                showlegend=True))
    
    layout = dict(
            xaxis = dict(
            showgrid= False,
            zeroline= False,
            rangeslider=dict(
            visible=True
            ),
            type='date',
            rangeselector = dict(
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
                )
            ),
            yaxis = {
            "showgrid": True,
            "zeroline": True,
            },
            margin=dict(l=30, r=30, b=0, t=40),
            hovermode="closest",
            plot_bgcolor="#F9F9F9",
            paper_bgcolor="#F9F9F9",
            legend=dict(font=dict(size=10),
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1)
            )
    
    # data must be a list of objects and not a list of lists
    return {"data": data, 'layout':layout}

# gets the value from the dropdown and the pagination
@app.callback(Output('table', 'data'),
            [Input('ticker_dropdown', "value"),
            Input('table', "page_current"),
            Input('table', "page_size")])
def update_table(selected_tickers,page_current,page_size):
    "cuts the dataframe with the chosen tickers and showa only the rows which fits in the pagination"
    data = df.loc[df['Ticker'].isin(selected_tickers),['Adj Close','Ticker']]
    return data.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')

if __name__ == "__main__":
    app.run_server(debug=True)