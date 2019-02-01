"""Configuration of the app"""
# -*- coding: utf-8 -*-
# pylint: disable=C0103
import dash
import dash_html_components as html

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True


def indicator(text, id_value):
    """Returns top indicator div"""
    return html.Div(
        [
            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                id=id_value,
                className="indicator_value"
            ),
        ],
        className="four columns indicator",
    )
