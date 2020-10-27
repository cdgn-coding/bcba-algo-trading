import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

LOGO = "/bullish_logo.png"

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])

# make a reuseable navitem for the different examples
nav_item = dbc.NavItem(dbc.NavLink("Link", href="#"))

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

# this is the default navbar style created by the NavbarSimple component
default = dbc.NavbarSimple(
    children=[nav_item, dropdown],
    brand="Default",
    brand_href="#",
    sticky="top",
    className="mb-5",
)

# this example that adds a logo to the navbar brand
logo = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Logo", className="ml-2")),
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

app.layout = html.Div(logo)

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

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)