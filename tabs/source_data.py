""" All related to the content of the source tab"""
# -*- coding: utf-8 -*-
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_table
from app import app, indicator


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
                                ),
                                dcc.Dropdown(
                                    id='instrument_selection',
                                    options=[
                                        {'label': key, 'value': value}
                                        for key, value in INSTRUMENTS[DEF_OBSERVATORY].items()
                                    ],
                                    value=DEF_INSTRUMENT
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


def add_files_to_table(source, filenames):
    """ Add the a new file name and size to the table"""

    return html.Div([
        dash_table.DataTable(
            data=[{'source': source, 'file_name': filename, 'file_size': 0}
                  for filename in filenames],
            columns=[
                {'name': 'Source', 'id': 'source'},
                {'name': 'File name', 'id': 'file_name'},
                {'name': 'Size', 'id': 'file_size'}]
        ),
    ])


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
            indicator("Total size", "total_size_indicator"),
        ],
        className="row",
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
              [Input('upload_file', 'filename')])
def update_table(list_of_names):
    """ Return a table with new info"""
    children = None
    if list_of_names is not None:
        children = add_files_to_table("File", list_of_names)
    return children


@app.callback(
    Output("number_of_files_indicator", "children"), [Input('upload_file', 'filename')])
def number_of_files_indicator_callback(filenames):
    """It updates the number of files indicator"""
    if filenames:
        number_of_files = len(filenames)
        return number_of_files
