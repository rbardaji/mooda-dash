""" All related to the content of the source tab"""
# -*- coding: utf-8 -*-
import json
import base64
import io
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table
from mooda import WaterFrame
from app import app, indicator


_DEBUG = True

PATH_EMSO = r"C:\Users\rbard\Google Drive\ok\EMSO-ERIC\server\www\html\data"
# The info is saved into dicts. It is not the best option. They could be saved into a DB
PARAMETERS = {
    'obsea': {
        'ctd': {
            'Water temperature': 'TEMP',
            'Salinity': 'PSAL',
            'Depth': 'MPMN',
            'Conductivity': 'CNDC',
            'Sound velocity': 'SVEL'
        },
        'tsunami': {
            'Pressure': 'PRES'
        },
        'oxi': {
            'Water temperature': 'TEMP',
            'Dissolved oxygen': 'DOX2',
            'Oxygen saturation': 'OSAT'
        },
        'tur': {
            'Turbidity': 'TUR4',
        },
    }
}

INSTRUMENTS = {
    'obsea': {
        'CTD': 'ctd',
        'Tsunami meter': 'tsunami',
        'Oximeter': 'oxi',
        'Turbidity meter': 'tur'
    }
}

OBSERVATORY = {
    'OBSEA Test Site': 'obsea',
}

DOWNLOAD_FILES = {
    'obsea': {
        'ctd': 'OS_OBSEA_2016120120170426_R_37-14998',
        'tsunami': 'OS_OBSEA_2016120120170426_R_SBE54-0049',
        'oxi': 'OS_OBSEA_2016120120170426_R_4381-606',
        'tur': 'OS_OBSEA_2016120120170426_R_NTURTD-648',
    }
}

# Definition of default values of the web app
DEF_OBSERVATORY = OBSERVATORY[list(OBSERVATORY.keys())[0]]
DEF_INSTRUMENT = INSTRUMENTS[DEF_OBSERVATORY][list(INSTRUMENTS[DEF_OBSERVATORY].keys())[0]]
DEF_PARAMETER = PARAMETERS[DEF_OBSERVATORY][DEF_INSTRUMENT]


def modal():
    """
    Modal layout. Hidden by defauld.

    Returns
    -------
        layout_modal: dash_html_component
            Layout of the modal
    """
    layout_modal = html.Div(
        html.Div(
            [
                html.Div(
                    [
                        # modal header
                        html.Div(
                            [
                                html.Span(
                                    "New dataset",
                                    style={
                                        "color": "#506784",
                                        "fontWeight": "bold",
                                        "fontSize": "20",
                                    },
                                ),
                                # x button
                                html.Span(
                                    "×",
                                    id="source_modal_close",
                                    n_clicks=0,
                                    style={
                                        "float": "right",
                                        "cursor": "pointer",
                                        "marginTop": "0",
                                        "marginBottom": "17",
                                    },
                                ),
                            ],
                            className="row",
                            style={"borderBottom": "1px solid #C8D4E3"},
                        ),

                        # From files
                        html.Div(
                            [
                                html.P(
                                    children="From files:",
                                    style={'textAlign': 'left'},
                                ),
                                # Drag and drop
                                dcc.Upload(
                                    id='upload_file',
                                    children=html.Div([
                                        'Drag and Drop or ',
                                        html.A('Select Files')
                                    ]),
                                    style={
                                        'width': '100%',
                                        'height': '60px',
                                        'lineHeight': '60px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '10px'
                                    },
                                    # Allow multiple files to be uploaded
                                    multiple=True
                                ),
                            ]
                        ),

                        # From Pangea
                        html.Div(
                            [
                                html.P(
                                    children="From Pangea:",
                                    style={'textAlign': 'left'},
                                ),
                                dcc.Input(
                                    placeholder='Id of dataset',
                                    type='number',
                                    value='',
                                    id='id_pangea'
                                ),
                                html.Button('Add', id='button_pangea', className="add_with_input"),
                            ]
                        ),

                        # From EMSO
                        html.Div(
                            [
                                html.P(
                                    children="From EMSO:",
                                    style={'textAlign': 'left'},
                                ),
                                dcc.Dropdown(
                                    id='observatory_selection',
                                    options=[
                                        {'label': key, 'value': value}
                                        for key, value in OBSERVATORY.items()
                                    ],
                                    value=DEF_OBSERVATORY,
                                    clearable=False,
                                ),
                                dcc.Dropdown(
                                    id='instrument_selection',
                                    options=[
                                        {'label': key, 'value': value}
                                        for key, value in INSTRUMENTS[DEF_OBSERVATORY].items()
                                    ],
                                    value=DEF_INSTRUMENT,
                                    clearable=False,
                                ),
                                html.Button('Add', id='button_emso'),
                            ]
                        )
                    ],
                    className="modal-content",
                    style={"textAlign": "center", "border": "1px solid #C8D4E3"},
                )
            ],
            className="modal",
        ),
        id="source_modal",
        style={"display": "none"}
    )
    return layout_modal


def add_files_to_table(list_of_files):
    """ Add the a new file name and size to the table"""

    return html.Div([
        dash_table.DataTable(
            data=list_of_files,
            columns=[
                {'name': 'Source', 'id': 'source'},
                {'name': 'File name', 'id': 'file_name'},
                {'name': 'Memory usage (MBytes)', 'id': 'file_size'}]
        ),
    ])


def size_file(filename, content=None):
    """ It returns the memory usage of a WaterFrame"""
    if _DEBUG:
        print("In size_file():")
        print("  - filename:", filename)

    if content is None:
        file_location = filename
    else:
        _content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        file_location = io.BytesIO(decoded)

    size = 0
    wf_file = WaterFrame()
    if 'nc' in filename:
        # Assume that the user uploaded a netcdf file
        wf_file.from_netcdf(file_location)
    elif 'csv' in filename:
        # Assume that the user uploaded a csv file
        wf_file.from_csv(file_location)
    size = wf_file.memory_usage()
    return size


LAYOUT = [
    modal(),

    # top controls
    html.Div(
        [
            # add button
            html.Div(
                html.Span(
                    "Add new",
                    id="new_source",
                    n_clicks=0,
                    className="button add",
                ),
                className="two columns",
                style={"float": "right"},
            ),

            html.P(" "),
        ],
        className="row",
        style={"marginBottom": "10"},
    ),

    # indicators
    html.Div(
        [
            indicator("Sources", "source_indicator"),
            indicator("Number of files", "number_of_files_indicator"),
            indicator("Total size (MBytes)", "total_size_indicator"),
        ],
        className="row",
        style={"marginBottom": "10"}
    ),

    # Table
    html.Div(id='output_table'),
]


@app.callback(Output("source_modal", "style"), [Input("new_source", "n_clicks")])
def display_source_modal_callback(n_clicks):
    """ It displays or hide the modal"""
    if n_clicks > 0:
        return {"display": "block"}
    return {"display": "none"}


@app.callback(
    Output("new_source", "n_clicks"),
    [Input("source_modal_close", "n_clicks"),
     Input("button_emso", "n_clicks"),
     Input("button_pangea", "n_clicks"),
     Input('upload_file', 'filename')])
def close_modal_callback(n_clicks_close, n_clicks_emso, n_clicks_pangea, filename):
    """ It is used to close the nodal, sending a callback to display_source_modal_callback"""
    return 0


@app.callback(Output('output_table', 'children'),
              [Input('table_content_files', 'children'),
               Input('table_content_pangea', 'children'),
               Input('table_content_emso', 'children')])
def update_table(files, pangea, emso):
    """ Return a table with new info"""
    children = None
    list_files = []
    if files:
        list_files = json.loads(files)
    if pangea:
        list_files += json.loads(pangea)
    if emso:
        list_files += json.loads(emso)
    if list_files:
        children = add_files_to_table(list_files)
    return children


@app.callback(
    Output("number_of_files_indicator", "children"),
    [Input('table_content_files', 'children'),
     Input('table_content_pangea', 'children'),
     Input('table_content_emso', 'children')])
def number_of_files_indicator_callback(content_files, content_pangea, content_emso):
    """It updates the number of files indicator"""
    number_files = 0
    number_pangea = 0
    number_emso = 0
    if content_files:
        files = json.loads(content_files)
        number_files = len(files)
    if content_pangea:
        files = json.loads(content_pangea)
        number_pangea = len(files)
    if content_emso:
        files = json.loads(content_emso)
        number_emso = len(files)
    number_of_files = number_files + number_pangea + number_emso
    return number_of_files


@app.callback(
    Output('table_content_pangea', 'children'),
    [Input('button_pangea', 'n_clicks')],
    [State('table_content_pangea', 'children'),
     State('id_pangea', 'value')])
def update_table_content_pangea(pangea_clicks, actual_files, id_pangea):
    """
    It updates the children of the div with id table_content_pangea with a JSON of the list of
    files added from Pangea
    """
    if _DEBUG:
        print("In update_table_content_pangea():")
        print("  - actual_files:", actual_files)
        print("  - pangea_clicks", pangea_clicks)
        print("  - id_pangea", id_pangea)
    new_content = None
    list_files = []
    new_files = []
    if actual_files:
        list_files = json.loads(actual_files)
        if _DEBUG:
            print("  - list_files:", list_files)
    if pangea_clicks > 0 and id_pangea > 0:
        new_files = [{'source': 'Pangea', 'file_name': str(id_pangea), 'file_size': "0"}]
        if _DEBUG:
            print("  - new_files:", new_files)
    list_files += new_files
    if _DEBUG:
        print("  - list_files to new_content:", list_files)
    new_content = json.dumps(list_files)
    if _DEBUG:
        print("Out of update_table_content_pangea()")
    return new_content


@app.callback(
    Output('table_content_files', 'children'),
    [Input('upload_file', 'contents')],
    [State('upload_file', 'filename'),
     State('table_content_files', 'children')])
def update_table_content_files(content_files, filenames, actual_files):
    """
    It updates the children of the div with id table_content_files with a JSON of the list of
    files added from the PC
    """
    if _DEBUG:
        print("In update_table_content_files():")
        print("  - filenames:", filenames)
        print("  - actual_files:", actual_files)
    new_content = None
    list_files = []
    new_files = []
    if actual_files:
        list_files = json.loads(actual_files)
        if _DEBUG:
            print("  - actual_files:", list_files)
    if filenames:
        new_files = [{'source': 'File',
                      'file_name': filename,
                      'file_size': size_file(filename, content)/1000000}
                     for filename, content in zip(filenames, content_files)]
        if _DEBUG:
            print("    - new_files:", new_files)
    list_files += new_files
    if _DEBUG:
        print("  - new_content:", list_files)
    new_content = json.dumps(list_files)
    if _DEBUG:
        print("Out of update_table_content_files()")
    return new_content


@app.callback(
    Output('table_content_emso', 'children'),
    [Input('button_emso', 'n_clicks')],
    [State('table_content_emso', 'children'),
     State('observatory_selection', 'value'),
     State('instrument_selection', 'value')])
def update_table_content_emso(emso_clicks, actual_files, observatory, instrument):
    """
    It updates the children of the div with id table_content_emso with a JSON of the list of
    files added from EMSO
    """
    if _DEBUG:
        print("In update_table_content_emso():")
        print("  - emso_clicks:", emso_clicks)
        print("  - actual_files:", actual_files)
    new_content = None
    list_files = []
    new_files = []
    if actual_files:
        list_files = json.loads(actual_files)
        if _DEBUG:
            print("  - actual_files:", list_files)
    if emso_clicks > 0:
        filename = f'{observatory}_{instrument}'
        path = fr'{PATH_EMSO}\{observatory}\{DOWNLOAD_FILES[observatory][instrument]}.nc'
        new_files = [{'source': 'EMSO',
                      'file_name': filename,
                      'file_size': size_file(filename=path)/1000000}]
        if _DEBUG:
            print("    - new_files:", new_files)
    list_files += new_files
    if _DEBUG:
        print("  - new_content:", list_files)
    new_content = json.dumps(list_files)
    if _DEBUG:
        print("Out of update_table_content_emso()")
    return new_content


@app.callback(
    Output('source_indicator', 'children'),
    [Input('table_content_files', 'children'),
     Input('table_content_pangea', 'children'),
     Input('table_content_emso', 'children')])
def sources_indicator_callback(content_files, content_pangea, content_emso):
    """It updates the number of files indicator"""
    number_of_sources = 0
    if content_files:
        number_of_sources += 1
    if content_pangea:
        number_of_sources += 1
    if content_emso:
        number_of_sources += 1
    return number_of_sources


@app.callback(
    Output('total_size_indicator', 'children'),
    [Input('table_content_files', 'children'),
     Input('table_content_pangea', 'children'),
     Input('table_content_emso', 'children')])
def size_indicator_callback(content_files, content_pangea, content_emso):
    """It updates the number of files indicator"""
    total_size = 0
    files = []
    if content_files:
        files = json.loads(content_files)
    if content_emso:
        files = json.loads(content_emso)
    if content_pangea:
        files = json.loads(content_pangea)
    for line in files:
        total_size += line['file_size']
    return total_size
