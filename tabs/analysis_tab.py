""" All related to the content of the analysis tab"""
# -*- coding: utf-8 -*-
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app, indicator

_DEBUG = True

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
        ],
        className="row",
        style={"marginBottom": "10"},
    ),

    # indicators row
    html.Div(
        [
            indicator("Source", "source_name_indicator"),
            indicator("Parameters", "parameters_indicator"),
            indicator("Memory usage (MBytes)", "memory_indicator"),
        ],
        className="row",
    ),

    # charts row div
    html.Div(
        [
            html.Div(
                [
                    html.P("Metadata"),
                    dcc.Markdown(
                        id="metadata",
                        children="Metadata example"
                    ),
                ],
                className="four columns chart_div"
            ),

            html.Div(
                [
                    html.P("Other information"),
                    dcc.Markdown(
                        id="info",
                        children="Info example"
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


@app.callback(
    Output('source_input', 'options'),
    [Input('table_content_files', 'children'),
     Input('table_content_pangea', 'children'),
     Input('table_content_emso', 'children')])
def source_input_options(content_files, content_pangea, content_emso):
    """It updates the source options"""
    options = []
    if content_files:
        files = json.loads(content_files)
        options += [{"label": line['file_name'], "value": line['file_name']} for line in files]
    if content_emso:
        files = json.loads(content_emso)
        options += [{"label": line['file_name'], "value": line['file_name']} for line in files]
    if content_pangea:
        files = json.loads(content_pangea)
        options += [{"label": line['file_name'], "value": line['file_name']} for line in files]
    return options


@app.callback(
    Output("source_name_indicator", "children"),
    [Input("source_input", "value")],
    [State('table_content_files', 'children'),
     State('table_content_pangea', 'children'),
     State('table_content_emso', 'children')]
)
def update_source_name_indicator(source, content_files, content_pangea, content_emso):
    source_indicator = ""
    if content_files:
        files = json.loads(content_files)
        for line in files:
            if line['file_name'] == source:
                source_indicator = "File"
    if content_pangea:
        files = json.loads(content_pangea)
        for line in files:
            if line['file_name'] == source:
                source_indicator = "Pangea"
    if content_emso:
        files = json.loads(content_emso)
        for line in files:
            if line['file_name'] == source:
                source_indicator = "EMSO"
    return source_indicator


@app.callback(
    Output("parameters_indicator", "children"),
    [Input("source_input", "value")],
    [State('table_content_files', 'children'),
     State('table_content_pangea', 'children'),
     State('table_content_emso', 'children')])
def update_parameters_indicator(source, content_files, content_pangea, content_emso):
    parameter_indicator = ""
    if content_files:
        files = json.loads(content_files)
        for line in files:
            if line['file_name'] == source:
                parameter_indicator = line['num_parameters']
    if content_pangea:
        files = json.loads(content_pangea)
        for line in files:
            if line['file_name'] == source:
                parameter_indicator = line['num_parameters']
    if content_emso:
        files = json.loads(content_emso)
        for line in files:
            if line['file_name'] == source:
                parameter_indicator = line['num_parameters']
    return parameter_indicator


@app.callback(
    Output("memory_indicator", "children"),
    [Input("source_input", "value")],
    [State('table_content_files', 'children'),
     State('table_content_pangea', 'children'),
     State('table_content_emso', 'children')])
def update_memory_indicator(source, content_files, content_pangea, content_emso):
    memory_indicator = 0
    if content_files:
        files = json.loads(content_files)
        for line in files:
            if line['file_name'] == source:
                memory_indicator = line['file_size']
    if content_pangea:
        files = json.loads(content_pangea)
        for line in files:
            if line['file_name'] == source:
                memory_indicator = line['file_size']
    if content_emso:
        files = json.loads(content_emso)
        for line in files:
            if line['file_name'] == source:
                memory_indicator = line['file_size']
    return memory_indicator


@app.callback(
    Output("metadata", "children"),
    [Input("source_input", "value")],
    [State('table_content_files', 'children'),
     State('table_content_pangea', 'children'),
     State('table_content_emso', 'children')])
def update_metadata(source, content_files, content_pangea, content_emso):

    if _DEBUG:
        print("In update_metadata():")
        print("  - source:", source)

    metadata_text = ""
    if content_files:
        files = json.loads(content_files)
        for line in files:
            if line['file_name'] == source:
                metadata_text = line['metadata']
    if content_pangea:
        files = json.loads(content_pangea)
        for line in files:
            if line['file_name'] == source:
                metadata_text = line['metadata']
    if content_emso:
        files = json.loads(content_emso)
        for line in files:
            if line['file_name'] == source:

                if _DEBUG:
                    print("  - It is from EMSO")

                metadata_text = line['metadata']
    if _DEBUG:
        print("  - metadata_text:", metadata_text)
        print("Out of update_metadata()")
    return metadata_text


@app.callback(
    Output("info", "children"),
    [Input("source_input", "value")],
    [State('table_content_files', 'children'),
     State('table_content_pangea', 'children'),
     State('table_content_emso', 'children')])
def update_info(source, content_files, content_pangea, content_emso):

    if _DEBUG:
        print("In update_info():")
        print("  - source:", source)

    info_text = ""
    if content_files:
        files = json.loads(content_files)
        for line in files:
            if line['file_name'] == source:
                info_text = line['info']
    if content_pangea:
        files = json.loads(content_pangea)
        for line in files:
            if line['file_name'] == source:
                info_text = line['info']
    if content_emso:
        files = json.loads(content_emso)
        for line in files:
            if line['file_name'] == source:

                if _DEBUG:
                    print("  - It is from EMSO")

                info_text = line['info']
    if _DEBUG:
        print("Out of update_metadata()")
    return info_text
