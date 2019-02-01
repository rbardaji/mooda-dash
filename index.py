"""Main layout of the app. From here we are going to turn on the server"""
# -*- coding: utf-8 -*-
# pylint: disable=C0103
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from app import app
from tabs import source_data

app.layout = html.Div(
    [
        # Header
        html.Div(
            children=[
                html.Span("Module for Ocean Observatory Data Analysis", className='app-title'),
                html.Div(
                    html.Img(src='http://193.144.35.225/img/logo/logo-EMSO-ERIC.png',
                             height="100%"), style={"float": "right", "height": "100%"})
            ],
            className="header"
        ),

        # tabs
        html.Div([
            dcc.Tabs(
                id="tabs",
                style={"height": "20", "verticalAlign": "middle"},
                children=[
                    dcc.Tab(label="Source", value="source_tab"),
                    dcc.Tab(label="Analysis", value="analysis_tab"),
                    dcc.Tab(label="Code", value="code_tab")
                ],
                value="source_tab",
            )]),

        # Tab content
        html.Div(id="tab_content", style={"margin": "2% 3%"}),

        # css
        # html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",
        # rel="stylesheet"),
        # html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/
        # 2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
        # html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
        # html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
        # html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
        # html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw
        # /cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
    ],
    className="row",
    style={"margin": "0%"}
)


@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def render_content(tab):
    """Update what you see on screen when changing tab"""
    if tab == "source_tab":
        return source_data.LAYOUT
    elif tab == "analysis_tab":
        return 'analysis'
    elif tab == "code_tab":
        return 'code'
    else:
        return 'source'

if __name__ == '__main__':
    app.run_server(debug=True)
