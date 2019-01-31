"""Main layout of the app. From here we are going to turn on the server"""
# -*- coding: utf-8 -*-
# pylint: disable=C0103
import dash_core_components as dcc
import dash_html_components as html
from app import app

app.layout = html.Div(children=[
    # Header
    html.Div([
        html.Span("Module for Ocean Observatory Data Analysis", className='app-title'),
        html.Div(
            html.Img(src='http://193.144.35.225/img/logo/logo-EMSO-ERIC.png',
                     height="100%"), style={"float": "right", "height": "100%"})
    ], className="header"),

    # tabs
    html.Div([
        dcc.Tabs(
            id="tabs",
            style={"height": "20", "verticalAlign": "middle"},
            children=[
                dcc.Tab(label="Source", value="source_tab"),
                dcc.Tab(label="Analysis", value="analysis_tab"),
                dcc.Tab(id="code_tab", label="Code", value="code_tab"),
            ],
            value="source_tab",
        )], className="row tabs_div"),
])

if __name__ == '__main__':
    app.run_server(debug=True)
