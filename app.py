"""Configuration of the app"""
# -*- coding: utf-8 -*-
# pylint: disable=C0103
import dash

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
