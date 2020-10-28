# Import required libraries
import dash
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_table
import pathlib
from pandas.tseries.offsets import DateOffset

LOGO = "/assets/logo-dh-blanco.png"
GIT_LOGO = "/assets/github.png"

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../dashboard/dataset").resolve()
df = pd.read_pickle(DATA_PATH.joinpath("all_tickers_last_decade_features.pkl"))

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

page_index_link = dbc.NavItem(dbc.NavLink("Volver", href="/"))

page_2_link = dbc.NavItem(dbc.NavLink("Ver pronostico", href="/page-2"))

project_link = dbc.NavItem(dbc.NavLink("Ir al codigo del proyecto", href="https://github.com/cnexans/bcba-algo-trading", target="_blank"))

project_link_logo = html.A(
            html.Img(src=GIT_LOGO, style={ "height": "40px" }),
            href="https://github.com/cnexans/bcba-algo-trading",
            target="_blank",
            className="github-link"
        )


page_2_layout = html.Div([

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
                            [page_index_link, project_link_logo], className="ml-auto", navbar=True
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


    html.Div(
            [
           
            # Bloques
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [html.P("Month Variation"), html.H6(id="var_for_1")],
                                id="wells",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.P("Two Months Variation"), html.H6(id="var_for_2")],
                                id="wells",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.P("Three Months Variation"), html.H6(id="var_for_3")],
                                id="wells",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.P("Month Price"), html.H6(id="price_for_1")],
                                id="wells",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.P("Two Months Price"), html.H6(id="price_for_2")],
                                id="gas",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.P("Three Months Price"), html.H6(id="price_for_3")],
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
                    html.Div([
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
                        dcc.Graph(id="stock_for_chart")],
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

@app.callback([Output('var_for_1', 'children'),
            Output('var_for_2', 'children'),
            Output('var_for_3', 'children'),
            Output('price_for_1', 'children'),
            Output('price_for_2', 'children'),
            Output('price_for_3', 'children'),
            Output('strategy', 'children')],
            [Input('ticker_for_dropdown','value')])
def display_values(ticker):

    ticker_history = df.loc[df['Ticker'] == ticker]

    price = round(df.loc[df['Ticker'] == ticker].iloc[-1,:]['Adj Close'],2)

    import joblib

    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../dashboard/dataset").resolve()
    modelo_1 = joblib.load(DATA_PATH.joinpath("trained_model_Forward_Return_1m.joblib"))
    modelo_2 = joblib.load(DATA_PATH.joinpath("trained_model_Forward_Return_2m.joblib"))
    modelo_3 = joblib.load(DATA_PATH.joinpath("trained_model_Forward_Return_3m.joblib"))

    prediction_1 = modelo_1.predict(ticker_history)
    prediction_2 = modelo_2.predict(ticker_history)
    prediction_3 = modelo_3.predict(ticker_history)

    var_1 = str(round(prediction_1[-1],2))
    var_2 = str(round(prediction_2[-1],2))
    var_3 = str(round(prediction_3[-1],2))

    new_price_1 = round(price * (1 + prediction_1[-1]),2)
    new_price_2 = round(price * (1 + prediction_2[-1]),2)
    new_price_3 = round(price * (1 + prediction_3[-1]),2)

    # modificar en base a futuras predicciones
    advise = 'Sell'
    if new_price_3 > price:
        advise = 'Buy'

    return var_1, var_2, var_3, new_price_1, new_price_2, new_price_3, advise


from plotly.graph_objs import *

# get value from dropdown and draw it on the figure of the stock chart
@app.callback(Output('stock_for_chart','figure'),
            [Input('ticker_for_dropdown','value'),
            Input('price_for_1', 'children'),
            Input('price_for_2', 'children'),
            Input('price_for_3', 'children')])
def update_for_figure(ticker, price_for_1, price_for_2, price_for_3):
    "keep the figure (id=stock_chart) updated with the human selection (input=ticker_dropdown)"

    new = pd.DataFrame([float(price_for_1), float(price_for_2), float(price_for_3)],
        columns=['forecast'],
        index=[df.loc[df['Ticker'] == ticker].index[-1] + DateOffset(months=1),
            df.loc[df['Ticker'] == ticker].index[-1] + DateOffset(months=2),
            df.loc[df['Ticker'] == ticker].index[-1] + DateOffset(months=3)])

    trace1 = go.Scatter(x=df[df['Ticker'] == ticker].index,
                        y=df[df['Ticker'] == ticker]['Close'],
                        mode='lines',name= ticker +' prices')

    trace2 = go.Scatter(x=new.index,
                        y=new.forecast,
                        mode='markers',name=ticker+ ' forecast')

    graf = [trace1, trace2]

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
    return {"data": graf, 'layout':layout}


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