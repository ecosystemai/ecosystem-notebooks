# #http://127.0.0.1:8050/ 
# import dash
# import dash_table
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import State
# import plotly.graph_objects as go
# from datetime import date
# from dateutil.relativedelta import relativedelta
# import flask
# import ecosystem_scoring_pdash
# import json
# import base64
# import os
# import pandas as pd
# import dash_bootstrap_components as dbc
# import dash_trich_components as dtc
# import dash_pivottable
# import logging
# import time

# external_scripts = []
# external_stylesheets = ["https://use.fontawesome.com/releases/v5.15.1/css/all.css"]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# server = app.server

# app.layout = html.Div([
# 		dbc.Button("Test",
# 			outline=True, 
# 			color="primary",
# 			className="mr-1",
# 			id="test_button"
# 		),
# 		html.Label("", id= "test_label")
# 	], 
# 	style={"position": "relative"}
# )

# @app.callback(
# 	[
# 		dash.dependencies.Output("test_label", "children"),
# 	],
# 	[dash.dependencies.Input("test_button", "n_clicks")],
# 	# state=[
# 	# 	State(component_id="usecase_dropdown2", component_property="value"),
# 	# 	State(component_id="score_value_input2", component_property="value"),
# 	# ],
# 	prevent_initial_call=True)
# def test(n_clicks):
# 	time.sleep(3)
# 	return "Done"