#http://127.0.0.1:8050/ 
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import State
import plotly.graph_objects as go
from datetime import date
from dateutil.relativedelta import relativedelta
import flask
import ecosystem_scoring_pdash
import json
import base64
import os
import pandas as pd
import dash_bootstrap_components as dbc
import dash_trich_components as dtc
import dash_pivottable
import logging
import json


app = dash.Dash(__name__)
server = app.server
data = [{
		"category": "Module #1",
		"start": "2019-01-10",
		"end": "2019-01-13",
		"task": "Gathering requirements"
	}, {
		"category": "Module #1",
		"start": "2019-02-05",
		"end": "2019-04-18",
		"task": "Development"
	}, {
		"category": "Module #2",
		"start": "2019-01-08",
		"end": "2019-01-10",
		"task": "Gathering requirements"
	}, {
		"category": "Module #2",
		"start": "2019-01-12",
		"end": "2019-01-15",
		"task": "Producing specifications"
	}, {
		"category": "Module #2",
		"start": "2019-01-16",
		"end": "2019-02-05",
		"task": "Development"
	}, {
		"category": "Module #2",
		"start": "2019-02-10",
		"end": "2019-02-18",
		"task": "Testing and QA"
	}, {
		"category": ""
	}, {
		"category": "Module #3",
		"start": "2019-01-01",
		"end": "2019-01-19",
		"task": "Gathering requirements"
	}, {
		"category": "Module #3",
		"start": "2019-02-01",
		"end": "2019-02-10",
		"task": "Producing specifications"
	}, {
		"category": "Module #3",
		"start": "2019-03-10",
		"end": "2019-04-15",
		"task": "Development"
	}, {
		"category": "Module #3",
		"start": "2019-04-20",
		"end": "2019-04-30",
		"task": "Testing and QA",
	}, {
		"category": "Module #4",
		"start": "2019-01-15",
		"end": "2019-02-12",
		"task": "Gathering requirements",
	}, {
		"category": "Module #4",
		"start": "2019-02-25",
		"end": "2019-03-10",
		"task": "Development"
	}, {
		"category": "Module #4",
		"start": "2019-03-23",
		"end": "2019-04-29",
		"task": "Testing and QA"
}]
jdata = json.dumps(data)

data2 = [{
		"category": "Module #1",
		"start": "2019-01-10",
		"end": "2019-01-13",
		"task": "Gathering requirements"
	}, {
		"category": "Module #1",
		"start": "2019-02-05",
		"end": "2019-04-18",
		"task": "Development"
	}, {
		"category": "Module #2",
		"start": "2019-01-08",
		"end": "2019-01-10",
		"task": "Gathering requirements"
	}, {
		"category": "Module #2",
		"start": "2019-01-12",
		"end": "2019-01-15",
		"task": "Producing specifications"
	}, {
		"category": "Module #2",
		"start": "2019-01-16",
		"end": "2019-02-05",
		"task": "Development"
	}, {
		"category": "Module #2",
		"start": "2019-02-10",
		"end": "2019-02-18",
		"task": "Testing and QA"
}]
jdata2 = json.dumps(data2)

app.layout = html.Div([
		html.Label(jdata, id="amcs_data_buffer", hidden=True),
		html.Label("", id="amcs_output_div", hidden=True),
		html.Label("amcs_canvas_div", id="amcs_div_buffer", hidden=True),

		dbc.Card([
				dbc.CardHeader(
					dbc.Button("Filter Options", outline=True, color="link", id="amcs_collapse_button", style={"height": "100%", "width": "100%"}),
				),
				dbc.Collapse(
					dbc.CardBody(
						html.Div([
								html.Label("Database"),
								dcc.Dropdown(
									id="amcs_database_dropdown",
									clearable=False,
								),
								html.Br(),
								html.Label("Collection"),
								dcc.Dropdown(
									id="amcs_collection_dropdown",
									clearable=False,
								),
								html.Br(),
								html.Label("Field"),
								html.Br(),
								dcc.Input(
									id="amcs_field_input",
									value="{}"
								),
								html.Br(),
								html.Br(),
								html.Label("Projections"),
								html.Br(),
								dcc.Input(
									id="amcs_projections_input",
									value="{}"
								),
								html.Br(),
								html.Br(),
								html.Label("Limit"),
								html.Br(),
								dcc.Input(
									id="amcs_limit_input",
									type="number",
									value=0
								),
								html.Br(),
								html.Br(),
								html.Label("Skip"),
								html.Br(),
								dcc.Input(
									id="amcs_skip_input",
									type="number",
									value=0
								),
								html.Br(),
								html.Br(),
								dbc.Button("Generate Graph", id="amcs_generate_button"),
							],
						),
					),
					id="amcs_collapse"
				)
			]
		),
		dbc.Card(
			dbc.CardBody([
					html.Div([], id="amcs_canvas_div", style={"height": "100%", "width": "100%"}),
				]
			),
			style={"height": "900px", "width": "100%"}
		),
	], 
	style={"position": "relative"}
)

app.clientside_callback(
	dash.dependencies.ClientsideFunction(
		namespace="clientside",
		function_name="amcharter_serpentine"
	),
	dash.dependencies.Output("amcs_output_div", "children"),
	[
		dash.dependencies.Input("amcs_data_buffer", "children"),
	],
	state=[
		State(component_id="amcs_div_buffer", component_property="children"),
	],
	prevent_initial_call=True)

@app.callback(
	dash.dependencies.Output("amcs_collapse", "is_open"),
	[
		dash.dependencies.Input("amcs_collapse_button", "n_clicks")
	],
	state=[
		State(component_id="amcs_collapse", component_property="is_open"),
	],
	prevent_initial_call=True
)
def amcs_toggle_collapse(n_clicks, is_open):
	if is_open:
		return False
	return True


@app.callback(
	dash.dependencies.Output("amcs_database_dropdown", "options"),
	[	
		dash.dependencies.Input("login_status", "children")
	],
	prevent_initial_call=True)
def callback_login3(children):
	try:
		databases = sd.get_prediction_databases()
		new_databases = []
		for entry in databases["databases"]:
			new_databases.append(entry["name"])
		return convert_list(new_databases)
	except Exception as e:
		print(e)
		return []

@app.callback(
	[
		dash.dependencies.Output("amcs_collection_dropdown", "options"),
		dash.dependencies.Output("amcs_collection_dropdown", "value"),
	],
	[	
		dash.dependencies.Input("amcs_database_dropdown", "value")
	],
	prevent_initial_call=True)
def callback_amcs_database(database):
	try:
		collections = sd.get_prediction_collections(database)
		new_collections = []
		for entry in collections["collection"]:
			new_collections.append(entry["name"])
		return convert_list(new_collections), None
	except Exception as e:
		print(e)
		return [], None

@app.callback(
	[
		dash.dependencies.Output("amcs_data_buffer", "children"),
	],
	[dash.dependencies.Input("amcs_generate_button", "n_clicks")],
	state=[
		State(component_id="amcs_database_dropdown", component_property="value"),
		State(component_id="amcs_collection_dropdown", component_property="value"),
		State(component_id="amcs_field_input", component_property="value"),
		State(component_id="amcs_projections_input", component_property="value"),
		State(component_id="amcs_limit_input", component_property="value"),
		State(component_id="amcs_skip_input", component_property="value"),
	],
	prevent_initial_call=True)
def callback_find_button(n_clicks, database, collection, field, projections, limit, skip):
	if database == "" or database == None:
		return None
	if collection == "" or collection == None:
		return None
	outputs = sd.get_documents(database, collection, field, projections, limit, skip)
	global custom_graphing_adv_refresh
	custom_graphing_adv_refresh = True
	return json.dumps(outputs)
	

if __name__ == "__main__":
	app.run_server(debug=True)
