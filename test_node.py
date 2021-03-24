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

# logging.getLogger("werkzeug").setLevel(logging.ERROR)
# external_scripts = []
# external_stylesheets = ["https://use.fontawesome.com/releases/v5.15.1/css/all.css"]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)
server = app.server
data = [{
		"category": "Module #1",
		"start": "2019-01-10",
		"end": "2019-01-13",
		"colorindex": 0,
		"task": "Gathering requirements"
	}, {
		"category": "Module #1",
		"start": "2019-02-05",
		"end": "2019-04-18",
		"colorindex": 0,
		"task": "Development"
	}, {
		"category": "Module #2",
		"start": "2019-01-08",
		"end": "2019-01-10",
		"colorindex": 5,
		"task": "Gathering requirements"
	}, {
		"category": "Module #2",
		"start": "2019-01-12",
		"end": "2019-01-15",
		"colorindex": 5,
		"task": "Producing specifications"
	}, {
		"category": "Module #2",
		"start": "2019-01-16",
		"end": "2019-02-05",
		"colorindex": 5,
		"task": "Development"
	}, {
		"category": "Module #2",
		"start": "2019-02-10",
		"end": "2019-02-18",
		"colorindex": 5,
		"task": "Testing and QA"
	}, {
		"category": ""
	}, {
		"category": "Module #3",
		"start": "2019-01-01",
		"end": "2019-01-19",
		"colorindex": 9,
		"task": "Gathering requirements"
	}, {
		"category": "Module #3",
		"start": "2019-02-01",
		"end": "2019-02-10",
		"colorindex": 9,
		"task": "Producing specifications"
	}, {
		"category": "Module #3",
		"start": "2019-03-10",
		"end": "2019-04-15",
		"colorindex": 9,
		"task": "Development"
	}, {
		"category": "Module #3",
		"start": "2019-04-20",
		"end": "2019-04-30",
		"colorindex": 9,
		"task": "Testing and QA",
		"disabled2":False,
		"image2":"./assets/logo.png",
		"location":0
	}, {
		"category": "Module #4",
		"start": "2019-01-15",
		"end": "2019-02-12",
		"colorindex": 15,
		"task": "Gathering requirements",
		"disabled1":False,
		"image1":"./assets/logo.png"
	}, {
		"category": "Module #4",
		"start": "2019-02-25",
		"end": "2019-03-10",
		"colorindex": 15,
		"task": "Development"
	}, {
		"category": "Module #4",
		"start": "2019-03-23",
		"end": "2019-04-29",
		"colorindex": 15,
		"task": "Testing and QA"
}]
jdata = json.dumps(data)

data2 = [{
		"category": "Module #1",
		"start": "2019-01-10",
		"end": "2019-01-13",
		"colorindex": 0,
		"task": "Gathering requirements"
	}, {
		"category": "Module #1",
		"start": "2019-02-05",
		"end": "2019-04-18",
		"colorindex": 0,
		"task": "Development"
	}, {
		"category": "Module #2",
		"start": "2019-01-08",
		"end": "2019-01-10",
		"colorindex": 5,
		"task": "Gathering requirements"
	}, {
		"category": "Module #2",
		"start": "2019-01-12",
		"end": "2019-01-15",
		"colorindex": 5,
		"task": "Producing specifications"
	}, {
		"category": "Module #2",
		"start": "2019-01-16",
		"end": "2019-02-05",
		"colorindex": 5,
		"task": "Development"
	}, {
		"category": "Module #2",
		"start": "2019-02-10",
		"end": "2019-02-18",
		"colorindex": 5,
		"task": "Testing and QA"
}]
jdata2 = json.dumps(data2)

app.layout = html.Div([
		html.Label("hello"),
		html.Label(jdata, id="data_buffer", hidden=True),
		html.Label(jdata2, id="data_buffer2", hidden=True),
		dbc.Button("push", id="button"),
		dbc.Button("push2", id="button2"),
		html.Div([], id="test_div", style={"height": "900px", "width": "100%"}),
		html.Label("Poop", id="script"),
	], 
	style={"position": "relative"}
)

app.clientside_callback(
	dash.dependencies.ClientsideFunction(
		namespace="clientside",
		function_name="amcharterer"
	),
	dash.dependencies.Output("script", "children"),
	[
		dash.dependencies.Input("button", "n_clicks"),
		dash.dependencies.Input("button2", "n_clicks")
	],
	state=[
		State(component_id="data_buffer", component_property="children"),
		State(component_id="data_buffer2", component_property="children"),
	],
	prevent_initial_call=True)


if __name__ == "__main__":
	app.run_server(debug=True)
