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

logging.getLogger("werkzeug").setLevel(logging.ERROR)

ECO_LOGO = "./assets/favicon.ico"
CURRENT_YEAR = "2021"
VERSION = "0.5.9780"

sd = None
export_target="export_wow.csv"
tmp_dir = "tmp/"
export_tmp = tmp_dir + "dashboard_export.csv"
if not os.path.exists(tmp_dir):
	os.mkdir(tmp_dir)

def generate_toast(message, header, icon):
	return dbc.Toast(
		message,
		header=header,
		is_open=True,
		dismissable=True,
		icon=icon,
		duration=10000,
		style={"position": "fixed", "top": 66, "right": 10, "width": 350, "zIndex": 10}
	)

def json_flatten(jdict, key_prefix):
	rdict = {}
	for key in jdict.keys():
		key_add = "{}_{}".format(key_prefix,key)
		if key_prefix == "":
			key_add = key
		if type(jdict[key]) == dict:
			rdict.update(json_flatten(jdict[key], key_add))
		elif type(jdict[key]) == list:
			rdict.update(json_flatten(jdict[key][0], key_add))
		else:
			rdict[key_add] = jdict[key]
	return rdict

def convert_list(l):
	new_l = []
	for entry in l:
		new_l.append({"label": entry, "value": entry})
	new_l = sorted(new_l, key = lambda i: i["label"])
	return new_l

external_scripts = []
external_stylesheets = ["https://use.fontawesome.com/releases/v5.15.1/css/all.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

navbar = dbc.Navbar([
		dbc.Row(
			[
				dbc.Col(html.Img(src=ECO_LOGO, height="30px", width="30px"), md=3),
				dbc.Col(dbc.NavbarBrand("Dashboard", className="ml-2")),
			],
			align="center",
			no_gutters=True,
		),
	],
	color="white",
	sticky="top",
)

continuous_empty = html.Div([
		html.Label("Predictor type not acceptable.")
	],
	style={"height": "650px", "display": "none"},
	id="continuous_empty_div"
)

continuous_wellness = html.Div([
		html.Br(),
		html.Div([
				html.Label("Customer Data"),
				html.Br(),
				dbc.InputGroup(
					[
						dcc.Input(
							id="wellness_upload_customer_data",
							disabled=True,
							style={"width": "60%"}
						),
						dbc.InputGroupAddon(
							dcc.Upload(dbc.Button(html.I(className="fas fa-upload"), outline=True, color="primary"), id="wellness_customer_upload_picker", style={"display": "inline-block"}),
							addon_type="append",
						),
					]
				),
				html.Br(),
			],
			style={"border": "1px solid #dee2e6", "padding": "5px"}
		),
		html.Br(),
		dbc.Button("Process Uploads",
			outline=True, 
			color="primary",
			className="mr-1",
			id="wellness_process_uploads_button"
		)
	],
	style={"height": "650px", "display": "none"},
	id="continuous_wellness_div"
)

continuous_spend_personality = html.Div([
		html.Br(),
		html.Div([
				html.Label("Customer Data"),
				html.Br(),
				dbc.InputGroup(
					[
						dcc.Input(
							id="spend_personality_upload_customer_data",
							disabled=True,
							style={"width": "60%"}
						),
						dbc.InputGroupAddon(
							dcc.Upload(dbc.Button(html.I(className="fas fa-upload"), outline=True, color="primary"), id="spend_personality_customer_upload_picker", style={"display": "inline-block"}),
							addon_type="append",
						),
					]
				),
				html.Br(),
				html.Label("Transaction Data"),
				html.Br(),
				dbc.InputGroup(
					[
						dcc.Input(
							id="spend_personality_upload_transaction_data",
							disabled=True,
							style={"width": "60%"}
						),
						dbc.InputGroupAddon(
							dcc.Upload(dbc.Button(html.I(className="fas fa-upload"), outline=True, color="primary"), id="spend_personality_transaction_upload_picker", style={"display": "inline-block"}),
							addon_type="append",
						),
					]
				),
				html.Br(),
				html.Label("CTO Data"),
				html.Br(),
				dbc.InputGroup(
					[
						dcc.Input(
							id="spend_personality_upload_cto_data",
							disabled=True,
							style={"width": "60%"}
						),
						dbc.InputGroupAddon(
							dcc.Upload(dbc.Button(html.I(className="fas fa-upload"), outline=True, color="primary"), id="spend_personality_cto_upload_picker", style={"display": "inline-block"}),
							addon_type="append",
						),
					]
				),
				html.Br(),
			],
			style={"border": "1px solid #dee2e6", "padding": "5px"}
		),
		html.Br(),
		dbc.Button("Process Uploads",
			outline=True, 
			color="primary",
			className="mr-1",
			id="spend_personality_process_uploads_button"
		)
	],
	style={"height": "650px", "display": "none"},
	id="continuous_spend_personality_div"
)

login_component = html.Div([
		navbar,
		html.Div([
				dbc.Row(
					[
						dbc.Col([], md=4),
						dbc.Col(
							dbc.Card(
								dbc.CardBody([
										html.H3("Login Details"),
										dbc.Form(
											[
												dbc.FormGroup(
													[
														dbc.Label("Prediction Server URL"),
														dbc.Input(
															# placeholder="Enter Prediction Server URL", 
															id="ps_url",
															type="text",
															# value="http://demo.ecosystem.ai:3001/api"
															value="http://127.0.0.1:3001/api"
														),
													]
												),
												dbc.FormGroup(
													[
														dbc.Label("Prediction Server Username"),
														dbc.Input(
															# placeholder="Enter Prediction Server Username", 
															id="ps_username",
															type="text",
															value="user@ecosystem.ai"
														),
													]
												),
												dbc.FormGroup(
													[
														dbc.Label("Prediction Server Password"),
														dbc.Input(
															# placeholder="Enter Prediction Server Password", 
															id="ps_password",
															type="password",
															value="password"
														),
													]
												),
											]
										),
										dbc.Button("Login", outline=True, id="login_button", color="primary", className="mr-1"),
										html.Br(),
										html.Label("", id="login_status", style={"display": "none"}),
										html.Br(),
										html.Div(id="login_alert_div"),
										html.Br(),
										html.Label("ecosystem.Ai Dashboard {}".format(VERSION))
									]
								)
							),
							md=4
						),
						dbc.Col([], md=4),
					]
				)
			],
			style={"padding-left": "30px", "padding-right": "30px", "padding-top": "30px", "padding-bottom": "30px"}
		),
	],
	id="login_component",
	style={"display": "none"}
)

scoring_component = html.Div([
		navbar,
		html.Div([
				dbc.Row(
					[
						dbc.Col(
							html.Div([
									dbc.Card(
										dbc.CardBody([
												html.Label(html.B("Use Case Details"), style={"margin-bottom": "0rem"}),
											],
											style={"padding": "0.75rem"}
										),
									),
									html.Br(),
									dbc.Card(
										dbc.CardBody([	
												html.Div([
														html.Label("Use Case"),
														dcc.Dropdown(
															id="usecase_dropdown",
															clearable=False,
														),
														html.Br(),
														dbc.Button("Test Connection", outline=True, color="primary", id="test_conn_button"),
														html.Br(),
														html.Br(),
														html.Label("Find Filter"),
														html.Br(),
														dbc.InputGroup(
															[
																dcc.Input(
																	id="find_filter_input",
																	value="{}"
																),
																dbc.InputGroupAddon(
																	dbc.Button("Filter", outline=True, color="primary", id="filter_button"),
																	addon_type="append",
																),
															]
														),
														html.Br(),
														html.Label("Customer"),
														html.Div([
																dbc.Checklist(
																	id="customer_list",
																	options = [],
																	style={"padding-left": "5px"}
																),
															],
															style={"overflow-y": "scroll", "height": "180px", "border": "1px solid grey"}
														),
														html.Br(),
														html.Label("Score Value"),
														html.Br(),
														dbc.InputGroup(
															[
																dcc.Input(
																	id="score_value_input",
																	value=""
																),
																dbc.InputGroupAddon(
																	dbc.Button("Score", outline=True, color="primary", id="score_button"),
																	addon_type="append",
																),
															]
														),
														html.Br(),
														html.Label("", id="score_buffer", style={"display": "none"}),
														dcc.Upload(
															dbc.Button("Batch Score", outline=True, color="primary", className="mr-1"),
															id="batch_score_picker",
															style={"display": "inline-block"}
														)
													],
													style={"height": "693px"}
												)
											]
										)
									)
								],
								# style={"border": "5px solid grey", "width": "100%"}
							),
							md=3
						),
						dbc.Col(
							html.Div(
								[
									dbc.Card(
										dbc.CardBody([
												html.Label(html.B("Transaction Details"), style={"margin-bottom": "0rem"}),
											],
											style={"padding": "0.75rem"}
										),
									),
									html.Br(),
									dbc.Card(
										dbc.CardBody([
												html.Div([
														html.Div([
																dbc.ListGroup([], id="table_div", style={"overflow-y": "scroll", "max-height": "600px"})
															],
														)
													],
													style={"height": "693px"}
												)
											]
										)
									)
								],
								# style={"border": "5px solid grey", "width": "100%"}
							),
							md=5
						),
						dbc.Col(
							html.Div(
								[
									dbc.Card(
										dbc.CardBody([
												html.Label(html.B("Upload Data"), style={"margin-bottom": "0rem"}),
											],
											style={"padding": "0.75rem"}
										),
									),
									html.Br(),
									dbc.Card(
										dbc.CardBody(
											dbc.Tabs([
													dbc.Tab(
														html.Div([
																html.Br(),
																html.Div([
																		html.Label("Use Case Name"),
																		html.Br(),
																		dcc.Input(id="usecase_name"),
																		html.Br(),
																		html.Br(),
																		html.Label("Runtime URL"),
																		html.Br(),
																		dcc.Input(id="usecase_runtime_url"),
																		html.Br(),
																		html.Br(),
																		html.Label("Properties"),
																		dcc.Textarea(
																			id="properties_textarea",
																			style={"width": "100%", "height": "200px"},
																		),
																		html.Br(),
																		dcc.Upload(dbc.Button(html.I(className="fas fa-upload"), outline=True, color="primary"), id="upload_properties_picker", style={"display": "inline-block"}),
																	],
																	style={"border": "1px solid #dee2e6", "padding": "5px"}
																),
																html.Br(),
																dbc.Button("Upload",
																	outline=True, 
																	color="primary",
																	className="mr-1",
																	id="properties_button"
																),
															],
															style={"height": "650px"}
														),
														label="Use Case",
														tab_id="setup_properties"
													),
													dbc.Tab(
														html.Div([
																html.Br(),
																html.Div([
																		html.Label("Database"),
																		html.Br(),
																		dcc.Input(id="upload_database"),
																	],
																	style={"border": "1px solid #dee2e6", "padding": "5px"}
																),
																html.Br(),
																html.Div([
																		html.Label("Model"),
																		html.Br(),
																		dbc.InputGroup(
																			[
																				dcc.Input(
																					id="upload_model",
																					disabled=True,
																					style={"width": "60%"}
																				),
																				dbc.InputGroupAddon(
																					dcc.Upload(dbc.Button(html.I(className="fas fa-upload"), outline=True, color="primary"), id="upload_model_picker", style={"display": "inline-block"}),
																					addon_type="append",
																				),
																			]
																		),
																	],
																	style={"border": "1px solid #dee2e6", "padding": "5px"}
																),
																html.Br(),
																html.Div([
																		html.Label("Target Feature Store"),
																		html.Br(),
																		dcc.Input(id="upload_target_fs", style={"width": "60%"}),
																		html.Br(),
																		html.Br(),
																		html.Label("Feature Store"),
																		html.Br(),
																		dbc.InputGroup(
																			[
																				dcc.Input(
																					id="upload_fs",
																					disabled=True,
																					style={"width": "60%"}
																				),
																				dbc.InputGroupAddon(
																					dcc.Upload(dbc.Button(html.I(className="fas fa-upload"), outline=True, color="primary"), id="upload_fs_picker",),
																					addon_type="append",
																				),
																			]
																		),
																		html.Br(),
																		html.Label("Target Additional File"),
																		html.Br(),
																		dcc.Input(id="upload_target_ad", style={"width": "60%"}),
																		html.Br(),
																		html.Br(),
																		html.Label("Additional File"),
																		html.Br(),
																		dbc.InputGroup(
																			[
																				dcc.Input(
																					id="upload_ad",
																					disabled=True,
																					style={"width": "60%"}
																				),
																				dbc.InputGroupAddon(
																					dcc.Upload(dbc.Button(html.I(className="fas fa-upload"), outline=True, color="primary"), id="upload_ad_picker", style={"display": "inline-block"}),
																					addon_type="append",
																				),
																			]
																		),
																	],
																	style={"border": "1px solid #dee2e6", "padding": "5px"}
																),
																html.Br(),
																dbc.Button("Upload",
																	outline=True, 
																	color="primary",
																	className="mr-1",
																	id="files_button"
																)
															],
															style={"height": "650px"}
														),
														label="Files",
														tab_id="setup_files"
													),
													dbc.Tab(
														html.Div([continuous_spend_personality, continuous_wellness, continuous_empty],
															id="continuous_div"
														),
														label="Continuous",
														tab_id="upload_files"
													)
												]
											)
										)
									)
								],
								# style={"border": "5px solid grey", "width": "100%"}
							),
							md=4
						)
					],
				),
				html.Br(),
				html.Div([
						html.Div(
							[
								dbc.Card(
										dbc.CardBody([
												html.Label(html.B("Scoring Output"), style={"margin-bottom": "0rem"}),
											],
											style={"padding": "0.75rem"}
										),
									),
								html.Br(),
								dbc.Card(
									dbc.CardBody([
											dbc.Tabs([
													dbc.Tab(
														html.Div(
															id="scoring_div",
															style={"overflow-y": "scroll", "max-height": "580px"}
														),
														label="Scoring",
														tab_id="scoring_table"
													),
													dbc.Tab(
														# html.Div([],
														dbc.Textarea(
															id = "scoring_text_area",
															# className="tree",
															style= {"width": "100%", "height": "495px"}

														),
														label="Scoring Result",
														tab_id="scoring"
													),
													dbc.Tab(
														html.Div([
																dcc.Dropdown(
																	id="graph_dropdown",
																	options=[],
																	clearable=False
																),
																dcc.Graph(
																	id="graphing",
																	figure={}
																)
															],
															id="graphing_div",
															style= {"width": "100%", "height": "580px"}
														),
														label="Graph",
														tab_id="graph"
													),
													dbc.Tab(
														html.Div([
															],
															id="graphing_adv_div",
															style= {"width": "100%", "height": "580px"}
														),
														label="Advanced Graph",
														tab_id="graph_adv"
													),
												],
												id="tabs_scoring",
												active_tab="scoring_table",
											)
										]
									)
								)
							]
							# style={"width": "100%"}
						)
					],
					# style={"border": "5px solid grey", "width": "100%"}
				)
			],
			style={"padding-left": "30px", "padding-right": "30px", "padding-top": "30px", "padding-bottom": "30px"}
		)
	],
	id="scoring_component",
	style={"display": "none"}
)

batch_scoring_component = html.Div([
		navbar,
		html.Div([
				dbc.Row(
					[
						dbc.Col(
							html.Div([
									dbc.Card(
										dbc.CardBody([
												html.Label(html.B("Use Case Details"), style={"margin-bottom": "0rem"}),
											],
											style={"padding": "0.75rem"}
										),
									),
									html.Br(),
									dbc.Card(
										dbc.CardBody([
												html.Div([
														html.Label("Use Case"),
														dcc.Dropdown(
															id="usecase_dropdown2",
															# options=convert_list(sd.get_use_case_names()),
															clearable=False,
															# style={"font-size": "13px"}
														),
														html.Br(),
														html.Label("Find Filter"),
														html.Br(),
														dbc.InputGroup(
															[
																dcc.Input(
																	id="find_filter_input2",
																	value="{}"
																),
																dbc.InputGroupAddon(
																	dbc.Button("Filter", outline=True, color="primary", id="filter_button2"),
																	addon_type="append",
																),
															]
														),
														html.Br(),
														dbc.Button("Select All Filter", outline=True, color="primary", id="filter_button_score2"),
														html.Br(),
														html.Br(),
														html.Label("Customer"),
														html.Div([
																dbc.Checklist(
																	id="customer_list2",
																	options = [],
																	style={"padding-left": "5px"}
																),
															],
															style={"overflow-y": "scroll", "height": "240px", "border": "1px solid grey"}
														),
														html.Br(),
														html.Label("Score Value"),
														html.Br(),
														dbc.InputGroup(
															[
																dcc.Input(
																	id="score_value_input2",
																	value=""
																),
																dbc.InputGroupAddon(
																	dbc.Button("Score", outline=True, color="primary", id="score_button2"),
																	addon_type="append",
																),
															]
														),
														html.Br(),
														html.Label("", id="score_buffer2", style={"display": "none"}),
														dcc.Upload(
															dbc.Button("Batch Score", outline=True, color="primary", className="mr-1"),
															id="batch_score_picker2",
															style={"display": "inline-block"}
														),
														html.Br(),
														html.A(
															children=dbc.Button("Download Scoring Results", outline=True, color="primary", className="mr-1", id="download_score_button", disabled=True),
															download="",
															href="/export",
															target="_blank",
														)
													],
													style={"height": "750px"}
												)
											],
										)
									)
								],
							),
							md=3
						),
						dbc.Col(
							html.Div(
								[
									dbc.Card(
										dbc.CardBody([
												html.Label(html.B("Scoring Details"), style={"margin-bottom": "0rem"}),
											],
											style={"padding": "0.75rem"}
										),
									),
									html.Br(),
									dbc.Card(
										dbc.CardBody([
												html.Div([
														html.Div([
																dbc.ListGroup([], id="table_div2", style={"overflow-y": "scroll", "max-height": "730px"})
															],
														)
													],
													style={"height": "750px"}
												)
											]
										)
									)
								],
							),
							md=9
						),
					],
				),
			],
			style={"padding-left": "30px", "padding-right": "30px", "padding-top": "30px", "padding-bottom": "30px"}
		)
	],
	id="batch_scoring_component",
	style={"display": "none"}
)

footer = dbc.Card(
	dbc.CardBody([
			"Dashboard for ", html.A("ecosystem.Ai", href="https://ecosystem.ai/"), " ", CURRENT_YEAR
		],
		style={"padding-top": "2.0rem", "padding-bottom": "2.0rem"}
	)
)

app.layout = html.Div([
		dtc.SideBar([
				dtc.SideBarItem(id="id_1", label="Login", icon="fas fa-sign-in-alt", className="sideBarItem"),
				dtc.SideBarItem(id="id_2", label="Explore", icon="fas fa-compass", className="sideBarItem"),
				dtc.SideBarItem(id="id_3", label="Scoring", icon="fas fa-chart-line", className="sideBarItem")
			],
			className="sideBar"
		),
		html.Div([
				html.Div([], id="login_toast_div"),
				html.Div([], id="usecase_toast_div"),
				html.Div([], id="connection_test_toast_div"),
				html.Div([], id="files_toast_div"),
				html.Div([], id="spend_personality_continuous_toast_div"),
				html.Div([], id="wellness_continuous_toast_div"),
				html.Div([], id="score_toast_div"),
				html.Div([], id="score_toast_div2"),
				html.Div([], id="filter_toast_div"),
				html.Div([], id="filter_toast_div2"),
			],
			id="toast_div"
		),
		html.Div([login_component, scoring_component, batch_scoring_component, footer], id="page_content", className="page_content", style={"z-index": "-1"}),
	], 
	style={"position": "relative"}
)

@app.server.route("/export") 
def download_csv():
	return flask.send_file(export_tmp,
					mimetype="text/csv",
					attachment_filename=export_target,
					as_attachment=True)

@app.callback(
	dash.dependencies.Output("login_status", "children"),
	[dash.dependencies.Input("login_button", "n_clicks")],
	state=[
		State(component_id="ps_url", component_property="value"),
		State(component_id="ps_username", component_property="value"),
		State(component_id="ps_password", component_property="value"),
	],
	prevent_initial_call=True)
def callback_login(clicks, ps_url, ps_username, ps_password):
	global sd
	try:
		sd = ecosystem_scoring_pdash.ScoringDash(ps_url, ps_username, ps_password)
	except Exception as e:
		print(e)
		sd = None
		return "Error: Could not log in."
		
	return "Successfully logged in."

@app.callback(
	dash.dependencies.Output("login_toast_div", "children"),
	[dash.dependencies.Input("login_status", "children")],
	prevent_initial_call=True)
def callback_login3(children):
	if children[:5] == "Error":
		return generate_toast("Error: Could not log in.", "Error", "danger")
	return generate_toast("Successfully logged in.", "Success", "primary")

@app.callback(
	dash.dependencies.Output("usecase_dropdown", "options"),
	[	
		dash.dependencies.Input("login_status", "children"),
		dash.dependencies.Input("usecase_dropdown", "value"),
		dash.dependencies.Input("usecase_toast_div", "children")
	],
	prevent_initial_call=True)
def callback_login2(children, value, toast):
	try:
		sd.retrieve_properties()
		return convert_list(sd.get_use_case_names())
	except Exception as e:
		print(e)
		return {}

@app.callback(
	dash.dependencies.Output("usecase_dropdown2", "options"),
	[	
		dash.dependencies.Input("login_status", "children"),
		dash.dependencies.Input("usecase_dropdown", "value"),
		dash.dependencies.Input("usecase_toast_div", "children")
	],
	prevent_initial_call=True)
def callback_login2_2(children, value, toast):
	try:
		sd.retrieve_properties()
		return convert_list(sd.get_use_case_names())
	except Exception as e:
		print(e)
		return {}

@app.callback(
	dash.dependencies.Output("table_div", "children"),
	[
		dash.dependencies.Input("customer_list", "value"),
		dash.dependencies.Input("usecase_dropdown", "value")
	],
	prevent_initial_call=True)
def callback_customer_list(customer_list, usecase):
	ctx = dash.callback_context
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if trigger_id == "customer_list":
		if len(customer_list) < 1:
			return []
		customer = customer_list[-1]
		data = sd.dropdown_customer_eventhandler(customer, usecase)
		if len(data) > 1:
			df = pd.DataFrame(data)
			return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
		else:
			group_items = []
			for entry in data:
				for key in entry:
					# group_items.append(dbc.ListGroupItem("{}: {}".format(key, entry[key])))
					group_items.append(dbc.ListGroupItem(
						[
							dbc.ListGroupItemHeading(key),
							dbc.ListGroupItemText(entry[key]),
						]
					))
			return dbc.ListGroup(group_items)
	if trigger_id == "usecase_dropdown":
		return []

@app.callback(
	dash.dependencies.Output("find_filter_input", "value"),
	[
		dash.dependencies.Input("usecase_dropdown", "value")
	],
	prevent_initial_call=True)
def clear_find_filter(usecase):
	return "{}"

@app.callback(
	dash.dependencies.Output("find_filter_input2", "value"),
	[
		dash.dependencies.Input("usecase_dropdown2", "value")
	],
	prevent_initial_call=True)
def clear_find_filter2(usecase):
	global export_target
	export_target = "{}_export.csv".format(usecase)
	print(export_target)
	return "{}"

# Buttons
@app.callback(
	[
		dash.dependencies.Output("customer_list", "options"),
		dash.dependencies.Output("filter_toast_div", "children"),
	],
	[
		dash.dependencies.Input("filter_button", "n_clicks"),
		dash.dependencies.Input("usecase_dropdown", "value"),
	],
	state=[
		State(component_id="find_filter_input", component_property="value"),
	],
	prevent_initial_call=True)
def callback_find_filter_button(n_clicks, usecase, find_filter):
	ctx = dash.callback_context
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if trigger_id == "filter_button":
		if usecase == "" or usecase == None:
			return [], generate_toast("Error: Could not filter, usecase is not selected.", "Error", "danger")
		try:
			opts = sd.find_btn_eventhandler(usecase, find_filter)
			return opts, []
		except Exception as e:
			print(e)
			return [], generate_toast("Error: Could not filter: {}".format(e), "Error", "danger")

	if trigger_id == "usecase_dropdown":
		return [], []

@app.callback(
	[
		dash.dependencies.Output("customer_list2", "options"),
		dash.dependencies.Output("filter_toast_div2", "children"),
	],
	[
		dash.dependencies.Input("filter_button2", "n_clicks"),
		dash.dependencies.Input("usecase_dropdown2", "value")
	],
	state=[
		State(component_id="find_filter_input2", component_property="value"),
	],
	prevent_initial_call=True)
def callback_find_filter_button2(n_clicks, usecase, find_filter):
	ctx = dash.callback_context
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if trigger_id == "filter_button2":
		if usecase == "" or usecase == None:
			return [], generate_toast("Error: Could not filter, usecase is not selected.", "Error", "danger")
		try:
			opts = sd.find_btn_eventhandler(usecase, find_filter)
			return opts, []
		except Exception as e:
			print(e)
			return [], generate_toast("Error: Could not filter: {}".format(e), "Error", "danger")
	if trigger_id == "usecase_dropdown2":
		return [], []

@app.callback(
	[
		dash.dependencies.Output("score_buffer", "children"),
		dash.dependencies.Output("score_toast_div", "children")
	],
	[dash.dependencies.Input("score_button", "n_clicks")],
	state=[
		State(component_id="usecase_dropdown", component_property="value"),
		State(component_id="score_value_input", component_property="value"),
	],
	prevent_initial_call=True)
def callback_score_button(n_clicks, usecase, score_value):
	if score_value == "":
		return None, generate_toast("Error: Could not score: Score Value field is empty.", "Error", "danger")
	try:
		outputs = sd.score_btn_eventhandler(usecase, score_value)
		return outputs, []
	except Exception as e:
		print(e)
		return None, generate_toast("Error: Could not score: {}".format(e), "Error", "danger")


@app.callback(
	[
		dash.dependencies.Output("score_buffer2", "children"),
		dash.dependencies.Output("score_toast_div2", "children")
	],
	[dash.dependencies.Input("score_button2", "n_clicks")],
	state=[
		State(component_id="usecase_dropdown2", component_property="value"),
		State(component_id="score_value_input2", component_property="value"),
	],
	prevent_initial_call=True)
def callback_score_button2(n_clicks, usecase, score_value):
	if score_value == "":
		return None, generate_toast("Error: Could not score: Score Value field is empty.", "Error", "danger")
	try:
		outputs = sd.score_btn_eventhandler(usecase, score_value)
		return outputs, []
	except Exception as e:
		print(e)
		return None, generate_toast("Error: Could not score: {}".format(e), "Error", "danger")

# app.clientside_callback(
# 	dash.dependencies.ClientsideFunction(
# 		namespace="clientside",
# 		function_name="json_viewer"
# 	),
# 	dash.dependencies.Output("scoring_text_area", "style"),
# 	[dash.dependencies.Input("score_buffer", "children")],
# 	prevent_initial_call=True)

@app.callback(
	dash.dependencies.Output("scoring_text_area", "value"),
	[
		dash.dependencies.Input("score_buffer", "children")
	],
	prevent_initial_call=True)
def callback_score_buffer( score_b):
	try:
		j = json.loads(score_b)
		pj = json.dumps(j, indent=4, sort_keys=True)
		return pj
	except Exception as e:
		print(e)
		return None

@app.callback(
	dash.dependencies.Output("score_value_input", "value"),
	[
		dash.dependencies.Input("batch_score_picker", "contents"),
		dash.dependencies.Input("customer_list", "value"),
		dash.dependencies.Input("usecase_dropdown", "value")
	],
	state=[
		State(component_id="score_value_input", component_property="value"),
	],
	prevent_initial_call=True)
def batch_uploader(contents, customer_list, usecase, input_contents):
	ctx = dash.callback_context
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if trigger_id == "batch_score_picker":
		content_type, content_string = contents.split(",")
		decoded = base64.b64decode(content_string)
		text = decoded.decode("utf-8")
		custs = text.split("\n")
		return ",".join(custs)
	if trigger_id == "customer_list":
		return ",".join(customer_list)
	if trigger_id == "usecase_dropdown":
		return ""


@app.callback(
	dash.dependencies.Output("customer_list", "value"),
	[
		dash.dependencies.Input("usecase_dropdown", "value")
	],
	prevent_initial_call=True)
def refresh_customer_list(usecase):
	return []

@app.callback(
	dash.dependencies.Output("customer_list2", "value"),
	[
		dash.dependencies.Input("usecase_dropdown2", "value")
	],
	prevent_initial_call=True)
def refresh_customer_list2(usecase):
	return []

@app.callback(
	dash.dependencies.Output("score_value_input2", "value"),
	[
		dash.dependencies.Input("batch_score_picker2", "contents"),
		dash.dependencies.Input("customer_list2", "value"),
		dash.dependencies.Input("filter_button_score2", "n_clicks"),
		dash.dependencies.Input("usecase_dropdown2", "value")
	],
	state=[
		State(component_id="score_value_input2", component_property="value"),
		State(component_id="find_filter_input2", component_property="value"),
	],
	prevent_initial_call=True)
def batch_uploader2(contents, customer_list, n_clicks, usecase, input_contents, find_filter):
	ctx = dash.callback_context
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if trigger_id == "batch_score_picker2":
		content_type, content_string = contents.split(",")
		decoded = base64.b64decode(content_string)
		text = decoded.decode("utf-8")
		custs = text.split("\n")
		return ",".join(custs)
	if trigger_id == "customer_list2":		
		return ",".join(customer_list)
	if trigger_id == "filter_button_score2":
		opts = sd.find_btn_eventhandler(usecase, find_filter)
		score_list = []
		for result in opts:
			score_list.append(result["value"])
		s = ",".join(score_list)
		return s
	if trigger_id == "usecase_dropdown2":
		return ""

@app.callback(
	dash.dependencies.Output("graphing_div", "style"),
	[dash.dependencies.Input("tabs_scoring", "active_tab")],
	prevent_initial_call=True)
def tabs_content_graphing(tab):
	if tab == "graph":
		style = {"width": "98%", "height": "380px", "display": "block"}
	else:
		return {"display": "none"}

@app.callback(
	dash.dependencies.Output("graphing_adv_div", "style"),
	[dash.dependencies.Input("tabs_scoring", "active_tab")],
	prevent_initial_call=True)
def tabs_content_graphing(tab):
	if tab == "graph_adv":
		style = {"width": "98%", "height": "380px", "display": "block"}
	else:
		return {"display": "none"}

@app.callback(
	dash.dependencies.Output("graph_dropdown", "options"),
	[dash.dependencies.Input("score_buffer", "children")],
	prevent_initial_call=True)
def tabs_content_graphing2(children):
	try:
		jstr = json.loads(children)
		value = jstr[0]
		flat = json_flatten(value, "")
		l = list(flat.keys())
		return convert_list(l)
	except Exception as e:
		print(e)
		return None

@app.callback(
	dash.dependencies.Output("graphing", "figure"),
	[dash.dependencies.Input("graph_dropdown", "value")],
	state=[
		State(component_id="score_buffer", component_property="children"),
	],
	prevent_initial_call=True)
def tabs_content_graphing3(graph_dropdown_value, children):
	jstr = json.loads(children)
	data_points = []
	for value in jstr:
		flat = json_flatten(value, "")
		data_points.append(flat)
	xs = []
	ys = []
	y_string = graph_dropdown_value
	for value in data_points:
		xs.append("Customer: " + str(value["customer"]))
		ys.append(value[y_string])

	figure=dict(
		data=[
			dict(
				x=xs,
				y=ys,
				name=y_string,
				marker=dict(
					color="rgb(26, 118, 255)"
				)
			)
		],
		layout=dict(
			title="{} for Customers".format(y_string),
			xaxes={"type": "category"}
		)
	)
	return figure


@app.callback(
	dash.dependencies.Output("properties_textarea", "value"),
	[
		dash.dependencies.Input("upload_properties_picker", "contents"),
		dash.dependencies.Input("usecase_dropdown", "value")
	],
	prevent_initial_call=True)
def upload_properties(contents, usecase):
	ctx = dash.callback_context
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if trigger_id == "upload_properties_picker":
		return ecosystem_scoring_pdash.decode_text(contents)
	if trigger_id == "usecase_dropdown":
		return sd.get_properties(usecase)

@app.callback(
	dash.dependencies.Output("wellness_upload_customer_data", "value"),
	[dash.dependencies.Input("wellness_customer_upload_picker", "contents")],
	state=[
		State(component_id="wellness_customer_upload_picker", component_property="filename"),
	],
	prevent_initial_call=True)
def upload_prep_customers(contents, filename):
	return filename

@app.callback(
	dash.dependencies.Output("spend_personality_upload_customer_data", "value"),
	[dash.dependencies.Input("spend_personality_customer_upload_picker", "contents")],
	state=[
		State(component_id="spend_personality_customer_upload_picker", component_property="filename"),
	],
	prevent_initial_call=True)
def upload_prep_customers(contents, filename):
	return filename

@app.callback(
	dash.dependencies.Output("spend_personality_upload_transaction_data", "value"),
	[dash.dependencies.Input("spend_personality_transaction_upload_picker", "contents")],
	state=[
		State(component_id="spend_personality_transaction_upload_picker", component_property="filename"),
	],
	prevent_initial_call=True)
def upload_prep_transactions(contents, filename):
	return filename

@app.callback(
	dash.dependencies.Output("spend_personality_upload_cto_data", "value"),
	[dash.dependencies.Input("spend_personality_cto_upload_picker", "contents")],
	state=[
		State(component_id="spend_personality_cto_upload_picker", component_property="filename"),
	],
	prevent_initial_call=True)
def upload_prep_cto(contents, filename):
	return filename

@app.callback(
	dash.dependencies.Output("wellness_continuous_toast_div", "children"),
	[dash.dependencies.Input("wellness_process_uploads_button", "n_clicks")],
	state=[
		State(component_id="usecase_dropdown", component_property="value"),
		State(component_id="wellness_customer_upload_picker", component_property="filename"),
		State(component_id="wellness_customer_upload_picker", component_property="contents")
	],
	prevent_initial_call=True)
def callback_process_uploads(clicks, usecase, c_filename, c_content):
	try:
		sd.wellness_process_uploads(usecase, tmp_dir, c_filename, c_content)
		return generate_toast("Successfully processed new uploads.", "Success", "primary")
	except Exception as e:
		print(e)
		return generate_toast("Error: Could not process new uploads.", "Error", "danger")


@app.callback(
	dash.dependencies.Output("spend_personality_continuous_toast_div", "children"),
	[dash.dependencies.Input("spend_personality_process_uploads_button", "n_clicks")],
	state=[
		State(component_id="usecase_dropdown", component_property="value"),
		State(component_id="spend_personality_customer_upload_picker", component_property="filename"),
		State(component_id="spend_personality_customer_upload_picker", component_property="contents"),
		State(component_id="spend_personality_transaction_upload_picker", component_property="filename"),
		State(component_id="spend_personality_transaction_upload_picker", component_property="contents"),
		State(component_id="spend_personality_cto_upload_picker", component_property="filename"),
		State(component_id="spend_personality_cto_upload_picker", component_property="contents"),
	],
	prevent_initial_call=True)
def callback_process_uploads(clicks, usecase, c_filename, c_content, t_filename, t_content, cto_filename, cto_content):
	try:
		sd.spend_personality_process_uploads(usecase, tmp_dir + "to_upload.csv", tmp_dir, c_filename, c_content, tmp_dir, t_filename, t_content, tmp_dir, cto_filename, cto_content)
		return generate_toast("Successfully processed new uploads.", "Success", "primary")
	except Exception as e:
		print(e)
		return generate_toast("Error: Could not process new uploads.", "Error", "danger")

		
@app.callback(
	dash.dependencies.Output("connection_test_toast_div", "children"),
	[dash.dependencies.Input("test_conn_button", "n_clicks")],
	state=[
		State(component_id="usecase_dropdown", component_property="value"),
	],
	prevent_initial_call=True)
def test_connection(n_clicks, usecase_name):
	if sd.test_connection(usecase_name):
		return generate_toast("Connection Successful.", "Success", "primary")
	return generate_toast("Error: Could not connected to '{}' runtime server.".format(usecase_name), "Error", "danger")

@app.callback(
	dash.dependencies.Output("usecase_name", "value"),
	[dash.dependencies.Input("usecase_dropdown", "value")],
	prevent_initial_call=True)
def display_usecase_name(usecase):
	return usecase

@app.callback(
	dash.dependencies.Output("usecase_runtime_url", "value"),
	[dash.dependencies.Input("usecase_dropdown", "value")],
	prevent_initial_call=True)
def display_usecase_name(usecase):
	return sd.get_runtime_url(usecase)

@app.callback(
	dash.dependencies.Output("usecase_toast_div", "children"),
	[dash.dependencies.Input("properties_button", "n_clicks")],
	state=[
		State(component_id="usecase_name", component_property="value"),
		State(component_id="usecase_runtime_url", component_property="value"),
		State(component_id="properties_textarea", component_property="value"),
	],
	prevent_initial_call=True)
def process_properties(n_clicks, usecase_name, runtime_url, properties):
	try:
		sd.preprocess_properties(usecase_name, runtime_url, properties)
		return generate_toast("Successfully uploaded usecase: {}.".format(usecase_name), "Success", "primary")
	except Exception as e:
		print(e)
		return generate_toast("Error: Could not upload usecase: {}.".format(usecase_name), "Error", "danger")


@app.callback(
	dash.dependencies.Output("upload_model", "value"),
	[dash.dependencies.Input("upload_model_picker", "contents")],
	state=[
		State(component_id="upload_model_picker", component_property="filename"),
	],
	prevent_initial_call=True)
def upload_prep_model(contents, filename):
	return filename

@app.callback(
	dash.dependencies.Output("upload_fs", "value"),
	[dash.dependencies.Input("upload_fs_picker", "contents")],
	state=[
		State(component_id="upload_fs_picker", component_property="filename"),
	],
	prevent_initial_call=True)
def upload_prep_fs(contents, filename):
	return filename

@app.callback(
	dash.dependencies.Output("upload_ad", "value"),
	[dash.dependencies.Input("upload_ad_picker", "contents")],
	state=[
		State(component_id="upload_ad_picker", component_property="filename"),
	],
	prevent_initial_call=True)
def upload_prep_af(contents, filename):
	return filename

@app.callback(
	dash.dependencies.Output("graphing_adv_div", "children"),
	[dash.dependencies.Input("score_buffer", "children")],
	prevent_initial_call=True)
def tabs_content_graphing4(scoring_results):
	try:
		jstr = json.loads(scoring_results)
		data_points = []
		for value in jstr:
			flat = json_flatten(value, "")
			data_points.append(flat)
		df = pd.DataFrame(data_points)
		columns = list(df.columns)
		odd_header = columns[0]
		if odd_header == "customer":
			odd_header = columns[1]
		l = [columns]
		l.extend(df.values.tolist())
		graph = dash_pivottable.PivotTable(
			id="graphing_adv",
			data=l,
			cols=["customer"],
			colOrder="key_a_to_z",
			rows=[],
			rowOrder="key_a_to_z",
			rendererName="Line Chart",
			aggregatorName="List Unique Values",
			vals=[odd_header]
		)
		return graph
	except Exception as e:
		print(e)
		return None

@app.callback(
	dash.dependencies.Output("files_toast_div", "children"),
	[dash.dependencies.Input("files_button", "n_clicks")],
	state=[
		State(component_id="usecase_dropdown", component_property="value"),
		State(component_id="upload_database", component_property="value"),
		State(component_id="upload_target_fs", component_property="value"),
		State(component_id="upload_target_ad", component_property="value"),
		State(component_id="upload_model_picker", component_property="filename"),
		State(component_id="upload_model_picker", component_property="contents"),
		State(component_id="upload_fs_picker", component_property="filename"),
		State(component_id="upload_fs_picker", component_property="contents"),
		State(component_id="upload_ad_picker", component_property="filename"),
		State(component_id="upload_ad_picker", component_property="contents")
	],
	prevent_initial_call=True)
def upload_files(n_clicks, usecase, database, target_fs, target_ad, model_name, model_content, fs_name, fs_content, ad_name, ad_content):
	model_path = tmp_dir + model_name
	fs_path = tmp_dir + fs_name
	ad_path = tmp_dir + ad_name
	if ad_name == "" or ad_name == None or ad_content == "" or ad_content == None:
		try:
			sd.upload_use_case_files(usecase, database, model_path, fs_path, target_fs)
			return generate_toast("Successfully uploaded files.", "Success", "primary")
		except Exception as e:
			print(e)
			return generate_toast("Error: Could not upload files. {}".format(e), "Error", "danger")
	else:
		try:
			sd.upload_use_case_files(usecase, database, model_path, fs_path, target_fs, ad_path=ad_path, additional=target_ad)
			return generate_toast("Successfully uploaded files.", "Success", "primary")
		except Exception as e:
			print(e)
			return generate_toast("Error: Could not upload files. {}".format(e), "Error", "danger")


@app.callback(
	dash.dependencies.Output("scoring_div", "children"),
	[dash.dependencies.Input("score_buffer", "children")],
	prevent_initial_call=True)
def tabs_content_scoring_tab(children):
	try:
		jstr = json.loads(children)
		data_points = []
		for value in jstr:
			flat = json_flatten(value, "")
			data_points.append(flat)
		df = pd.DataFrame(data_points)
		return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
	except Exception as e:
		print(e)
		return None

@app.callback(
	dash.dependencies.Output("download_score_button", "disabled"),
	[dash.dependencies.Input("score_buffer2", "children")],
	prevent_initial_call=True)
def activate_downloader(children):
	if children != "" and children != None:
		return False
	return True
	

@app.callback(
	dash.dependencies.Output("table_div2", "children"),
	[dash.dependencies.Input("score_buffer2", "children")],
	prevent_initial_call=True)
def tabs_content_scoring_tab2(children):
	try:
		jstr = json.loads(children)
		data_points = []
		for value in jstr:
			flat = json_flatten(value, "")
			data_points.append(flat)
		df = pd.DataFrame(data_points)
		df.to_csv(export_tmp)
		return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
	except Exception as e:
		print(e)
		return None


@app.callback(
	dash.dependencies.Output("continuous_wellness_div", "style"),
	[
		dash.dependencies.Input("usecase_dropdown", "value")
	],
	prevent_initial_call=True
)
def toggle_continuous(dropdown_value):
	predictor = sd.get_predictor_type(dropdown_value)
	print("wellness: {}".format(predictor))
	if predictor == "wellness_score":
		return {"height": "650px"}
	return {"display": "none"}

@app.callback(
	dash.dependencies.Output("continuous_spend_personality_div", "style"),
	[
		dash.dependencies.Input("usecase_dropdown", "value")
	],
	prevent_initial_call=True
)
def toggle_continuous(dropdown_value):
	predictor = sd.get_predictor_type(dropdown_value)
	print("spend: {}".format(predictor))
	if predictor == "spending_personality":
		return {"height": "650px"}
	return {"display": "none"}

@app.callback(
	dash.dependencies.Output("continuous_empty_div", "style"),
	[
		dash.dependencies.Input("usecase_dropdown", "value")
	],
	prevent_initial_call=True
)
def toggle_continuous(dropdown_value):
	predictor = sd.get_predictor_type(dropdown_value)
	print("spend: {}".format(predictor))
	if predictor == "wellness_score":
		return {"display": "none"}
	if predictor == "spending_personality":
		return {"display": "none"}

	return {"height": "650px"}


@app.callback(
	dash.dependencies.Output("login_component", "style"),
	[
		dash.dependencies.Input("id_1", "n_clicks_timestamp"),
		dash.dependencies.Input("id_2", "n_clicks_timestamp"),
		dash.dependencies.Input("id_3", "n_clicks_timestamp"),
		dash.dependencies.Input("login_status", "children")
	],
)
def toggle_collapse(input1, input2, input3, login_status):
	ctx = dash.callback_context
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if trigger_id == "login_status":
		if login_status[:5] == "Error":			
			return {"background-color": "#edf1f7", "min-height": "90vh"}
		else:
			return {"display": "none"}
	else:
		if len(login_status) <= 2:
			return {"background-color": "#edf1f7", "min-height": "90vh"}
		elif login_status[:5] == "Error":
			return {"background-color": "#edf1f7", "min-height": "90vh"}
		else:
			btn_df = pd.DataFrame({"input1": [input1], "input2": [input2], "input3": [input3]})
			btn_df = btn_df.fillna(0)

			if btn_df.idxmax(axis=1).values == "input1" or btn_df.idxmax(axis=1).values == "input4":
				return {"background-color": "#edf1f7", "min-height": "90vh"}
			if btn_df.idxmax(axis=1).values == "input2":
				return {"display": "none"}
			if btn_df.idxmax(axis=1).values == "input3":
				return {"display": "none"}

@app.callback(
	dash.dependencies.Output("scoring_component", "style"),
	[
		dash.dependencies.Input("id_1", "n_clicks_timestamp"),
		dash.dependencies.Input("id_2", "n_clicks_timestamp"),
		dash.dependencies.Input("id_3", "n_clicks_timestamp"),
		dash.dependencies.Input("login_status", "children")
	],
	prevent_initial_call=True)
def toggle_collapse(input1, input2, input3, login_status):
	ctx = dash.callback_context
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if trigger_id == "login_status":
		if login_status[:5] == "Error":
			return {"display": "none"}
		else:
			return {"background-color": "#edf1f7", "min-height": "90vh"}
	else:
		if len(login_status) <= 2:
			return {"display": "none"}
		elif login_status[:5] == "Error":
			return {"display": "none"}
		else:
			btn_df = pd.DataFrame({"input1": [input1], "input2": [input2], "input3": [input3]})
			btn_df = btn_df.fillna(0)

			if btn_df.idxmax(axis=1).values == "input1":
				return {"display": "none"}
			if btn_df.idxmax(axis=1).values == "input2":
				return {"background-color": "#edf1f7", "min-height": "90vh"}
			if btn_df.idxmax(axis=1).values == "input3":
				return {"display": "none"}

@app.callback(
	dash.dependencies.Output("batch_scoring_component", "style"),
	[
		dash.dependencies.Input("id_1", "n_clicks_timestamp"),
		dash.dependencies.Input("id_2", "n_clicks_timestamp"),
		dash.dependencies.Input("id_3", "n_clicks_timestamp")
	],
	state=[
		State(component_id="login_status", component_property="children"),
	],
)
def toggle_collapse(input1, input2, input3, login_status):
	if len(login_status) <= 2:
		return {"display": "none"}
	elif login_status[:5] == "Error":
		return {"display": "none"}
	else:
		btn_df = pd.DataFrame({"input1": [input1], "input2": [input2], "input3": [input3]})
		btn_df = btn_df.fillna(0)

		if btn_df.idxmax(axis=1).values == "input1":
			return {"display": "none"}
		if btn_df.idxmax(axis=1).values == "input2":
			return {"display": "none"}
		if btn_df.idxmax(axis=1).values == "input3":
			return {"background-color": "#edf1f7", "min-height": "90vh"}

if __name__ == "__main__":
	app.run_server(debug=True)
