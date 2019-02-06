""" All related to the content of the analysis tab"""
# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
from app import indicator

LAYOUT = [

    # top controls
    html.Div(
        [
            html.Div(
                dcc.Dropdown(
                    id="source_input",
                    options=[
                        # {"label": "Example data", "value": "example"},
                    ],
                    value="",
                    clearable=False,
                ),
                className="two columns",
            ),

            html.Div(
                dcc.Dropdown(
                    id="resample_input",
                    options=[
                        {"label": "None", "value": "None"},
                        {"label": "Hourly", "value": "H"},
                        {"label": "Daily", "value": "D"},
                        {"label": "Weekly", "value": "W"},
                    ],
                    value="None",
                    clearable=False,
                ),
                className="two columns",
            ),
            html.Div(
                dcc.Dropdown(
                    id="source_dropdown",
                    options=[
                        {"label": "All sources", "value": "all_s"},
                        {"label": "Web", "value": "Web"},
                        {"label": "Word of Mouth", "value": "Word of mouth"},
                        {"label": "Phone Inquiry", "value": "Phone Inquiry"},
                        {"label": "Partner Referral", "value": "Partner Referral"},
                        {"label": "Purchased List", "value": "Purchased List"},
                        {"label": "Other", "value": "Other"},
                    ],
                    value="all_s",
                    clearable=False,
                ),
                className="two columns",
            ),

            # add button
            html.Div(
                html.Span(
                    "Show",
                    id="show_button",
                    n_clicks=0,
                    className="button button--primary add"
                ),
                className="two columns",
                style={"float": "right"},
            ),
        ],
        className="row",
        style={"marginBottom": "10"},
    ),

    # indicators row
    html.Div(
        [
            indicator("Won opportunities", "left_opportunities_indicator"),
            indicator("Open opportunities", "middle_opportunities_indicator"),
            indicator("Lost opportunities", "right_opportunities_indicator"),
        ],
        className="row",
    ),

    # charts row div
    html.Div(
        [
            html.Div(
                [
                    html.P("Leads count per state"),
                    dcc.Graph(
                        id="map",
                        style={"height": "90%", "width": "98%"},
                        config=dict(displayModeBar=False),
                    ),
                ],
                className="four columns chart_div"
            ),

            html.Div(
                [
                    html.P("Leads by source"),
                    dcc.Graph(
                        id="lead_source",
                        style={"height": "90%", "width": "98%"},
                        config=dict(displayModeBar=False),
                    ),
                ],
                className="four columns chart_div"
            ),

            html.Div(
                [
                    html.P("Converted Leads count"),
                    dcc.Graph(
                        id="converted_leads",
                        style={"height": "90%", "width": "98%"},
                        config=dict(displayModeBar=False),
                    ),
                ],
                className="four columns chart_div"
            ),
        ],
        className="row",
        style={"marginTop": "5"},
    ),
]
