#http://127.0.0.1:8050/ 
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import State
import plotly.graph_objects as go
from datetime import date
from datetime import timedelta
import flask
import json
import base64
import os
import pandas as pd
import dash_bootstrap_components as dbc
import dash_trich_components as dtc
import dash_pivottable
import logging
import dateutil

import ecosystem_scoring_pdash

logging.getLogger("werkzeug").setLevel(logging.ERROR)

ECO_LOGO = "./assets/favicon.ico"
CURRENT_YEAR = "2021"
VERSION = "0.5.9780"

graphing_adv_refresh = False
custom_graphing_adv_refresh = False
sd = None
export_target=""
tmp_dir = "tmp/"
export_tmp = tmp_dir + "dashboard_export.csv"
if not os.path.exists(tmp_dir):
	os.mkdir(tmp_dir)

class ButtonBusyState():
	def __init__(self):
		self.busy = False
		self.busy_changed = False

class ActiveStates():
	def __init__(self):
		# exp
		self.exp_score_button = ButtonBusyState()
		# scr
		# cg
		# amcs
		self.amcs_filter_button = ButtonBusyState()
		self.amcs_generate_button = ButtonBusyState()
		# amcd
		self.amcd_filter_button = ButtonBusyState()
		self.amcd_generate_button = ButtonBusyState()

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
		html.Label(
			"",
			id="navbar_pretitle",
			hidden=True
		),
		dbc.Row(
			[
				html.Img(src=ECO_LOGO, height="30px", width="30px"),
				dbc.NavbarBrand("Dashboard", id="navbar_title", className="ml-2", style={"padding-left": "3px"}),
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
															# value="http://127.0.0.1:3001/api"
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
															# value="user@ecosystem.ai"
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
															# value="password"
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

explore_component = html.Div([
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
																dbc.Card(
																	dbc.CardHeader(
																		dbc.Button("Advanced Options", outline=True, color="link", id="graphing_adv_collapse_button", style={"height": "100%", "width": "100%"}),
																	)
																),
																dbc.Collapse(
																	html.Div([
																			html.Br(),
																			html.Label("Add Field to Graph"),
																			dcc.Dropdown(
																				id="graph_adv_dropdown",
																				options=[],
																				multi=True
																			),
																		],
																	),
																	id="graphing_adv_collapse"
																),
																html.Div([],
																	id="graphing_adv_div",
																	style= {"width": "100%"}
																)
															],
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
	id="explore_component",
	style={"display": "none"}
)

scoring_component = html.Div([
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
	id="scoring_component",
	style={"display": "none"}
)

custom_graphing_component = html.Div([
		html.Div([
				dbc.Card([
						html.Label("", id="cg_find_buffer", style={"display": "none"}),
						dbc.CardHeader(
							dbc.Button("Options", outline=True, color="link", id="cg_collapse_button", style={"height": "100%", "width": "100%"}),
						),
						dbc.Collapse(
							dbc.CardBody([
									html.Label("Analysis"),
									html.Div([
											dbc.Row([
													dbc.Col([
															html.Label("Select Analysis ID"),
															html.Div([
																	html.Div(
																		dcc.Dropdown(
																			id="cg_analysis_dropdown",
																			clearable=False,
																		),
																	),
																],
															),
														],
														md=3
													),
													dbc.Col([
															html.Label("Analysis ID"),
															html.Div([
																	dbc.Input(
																		id="cg_analysis_input",
																		value="",
																	),
																],
															),
														],
														md=3
													),
													dbc.Col([
															html.Label("Description"),
															html.Div([
																	html.Div(
																		dbc.Input(
																			id="cg_description_input",
																			value="",
																		),
																	),
																],
															),
														],
														md=4
													),
													dbc.Col([
															html.Br(),
															html.Div([
																	dbc.Button(
																		"Save", 
																		outline=True, 
																		color="primary",
																		id="cg_analysis_save_button",
																		style={"width": "100px"}
																	),
																],
																style={"padding-top": "7px"}
															)
														],
														md=2
													),
												]
											),
										],
										style={"border": "1px solid #dee2e6", "padding": "5px"}
									),
									html.Br(),
									html.Label("Find"),
									html.Div([
											dbc.Row([
													dbc.Col([
															html.Label("Database"),
															html.Div([
																	html.Div(
																		dcc.Dropdown(
																			id="cg_database_dropdown",
																			clearable=False,
																		),
																		style={"width": "90%", "display": "inline-block"}
																	),
																	html.Div(
																		dbc.Button(
																			html.I(className="fas fa-sync"), 
																			outline=True, 
																			color="primary", 
																			id="cg_database_refresh_button", 
																			style={"height": "36px"}
																		),
																		style={"display": "inline-block", "vertical-align": "top"}
																	),
																],
															)
														],
														md=6
													),
													dbc.Col([
															html.Label("Collection"),
															dcc.Dropdown(
																id="cg_collection_dropdown",
																clearable=False,
															),
														],
														md=6
													),
												]
											),
											html.Br(),
											dbc.Row([
													dbc.Col([
															html.Label("Find"),
															html.Br(),
															dcc.Input(
																id="cg_field_input",
																value="{}",
																style={"width": "100%"}
															),
														],
														md=4
													),
													dbc.Col([
															html.Label("Projections"),
															html.Br(),
															dcc.Input(
																id="cg_projections_input",
																value="{}",
																style={"width": "100%"}
															),
														],
														md=4
													),
													dbc.Col([
															html.Label("Limit"),
															html.Br(),
															dcc.Input(
																id="cg_limit_input",
																type="number",
																value=100,
																style={"width": "100%"}
															),
														],
														md=2
													),
													dbc.Col([
															html.Label("Skip"),
															html.Br(),
															dcc.Input(
																id="cg_skip_input",
																type="number",
																value=0,
																style={"width": "100%"}
															),
														],
														md=2
													)
												]
											),
											html.Br(),
											dbc.Button("Find Data",
												outline=True, 
												color="primary",
												className="mr-1",
												id="cg_find_button"
											)
										],
										style={"border": "1px solid #dee2e6", "padding": "5px"}
									),
									html.Br(),
									html.Label("Selector"),
									html.Div([
											dbc.Row([
													dbc.Col([
															html.Label("Value"),
															html.Br(),
															dcc.Input(
																id="cg_adv_graph_value_input",
																value="",
																style={"width": "100%"}
															),
														],
														md=4
													),
												]
											),
										],
										style={"border": "1px solid #dee2e6", "padding": "5px"}
									),
								]
							),
							id="cg_collapse",
							is_open=True
						)
					]
				),
				html.Div(
					[
						dbc.Card(
							dbc.CardBody([
									html.Div([
											dbc.Tabs([
													dbc.Tab(
														html.Div(
															id="cg_results_div",
															style={"overflow-y": "scroll", "max-height": "700px"}
														),
														label="Results",
														tab_id="cg_table"
													),
													dbc.Tab(
														dbc.Textarea(
															id = "cg_text_area",
															# className="tree",
															style= {"width": "100%", "height": "700px"}

														),
														label="Raw Results",
														tab_id="cg_raw"
													),
													dbc.Tab(
														html.Div([
																dbc.Card(
																	dbc.CardHeader(
																		dbc.Button("Advanced Options", outline=True, color="link", id="cg_adv_collapse_button", style={"height": "100%", "width": "100%"}),
																	)
																),
																dbc.Collapse(
																	html.Div([
																			dcc.Dropdown(
																				id="cg_graph_adv_dropdown",
																				options=[],
																				multi=True
																			)
																		],
																	),
																	id="cg_adv_collapse"
																),
																html.Div([
																		dbc.Row([
																				dbc.Col([
																						html.Div([
																								dash_pivottable.PivotTable(
																									id="cg_adv_table_metadata",
																									data=[],
																									cols=[],
																									colOrder="key_a_to_z",
																									rows=[],
																									rowOrder="key_a_to_z",
																									rendererName="Line Chart",
																									aggregatorName="List Unique Values",
																									vals=[],
																									unusedOrientationCutoff="Infinity",
																									hiddenAttributes=[],
																								)
																							],
																							hidden=True,
																						),
																						html.Div([
																								dash_pivottable.PivotTable(
																									id="cg_adv_table",
																									data=[],
																									cols=[],
																									colOrder="key_a_to_z",
																									rows=[],
																									rowOrder="key_a_to_z",
																									rendererName="Line Chart",
																									aggregatorName="List Unique Values",
																									vals=[],
																									unusedOrientationCutoff="Infinity",
																									hiddenAttributes=[],
																								)
																							],
																							id="cg_adv_div",
																							style={"width": "100%"}
																						),
																					],
																					# style={"height": "675px"},
																					md=11
																				),
																				dbc.Col([
																						dbc.Textarea(
																							id="cg_notes_textarea",
																							className="mb-3",
																							placeholder="Notes...",
																							style={"height": "675px"}
																						)
																					],
																					md=1
																				)
																			]
																		)
																	],
																),
															],
														),
														label="Advanced Graph",
														tab_id="cg_adv"
													),
												],
												id="cg_tabs",
												active_tab="cg_table",
											)
										],
										id="cg_tab_div",
										# style={"height": "750px"}
									)
								]
							)
						)
					],
				),
			],
			style={"padding-left": "30px", "padding-right": "30px", "padding-top": "30px", "padding-bottom": "30px"}
		)
	],
	id="custom_graphing_component",
	style={"display": "none"}
)


amcs_component = html.Div([
		html.Div([
				html.Label("", id="amcs_data_buffer", hidden=True),
				html.Label("", id="amcs_data_prebuffer", hidden=True),
				html.Label("", id="amcs_output_div", hidden=True),
				html.Label("amcs_canvas_div", id="amcs_div_buffer", hidden=True),

				dbc.Card([
						dbc.CardHeader(
							dbc.Button("Options", outline=True, color="link", id="amcs_collapse_button", style={"height": "100%", "width": "100%"}),
						),
						dbc.Collapse(
							dbc.CardBody([
									html.Label("Analysis"),
									html.Div([
											dbc.Row([
													dbc.Col([
															html.Label("Select Analysis ID"),
															html.Div([
																	html.Div(
																		dcc.Dropdown(
																			id="amcs_analysis_dropdown",
																			clearable=False,
																		),
																	),
																],
															),
														],
														md=3
													),
													dbc.Col([
															html.Label("Analysis ID"),
															html.Div([
																	dbc.Input(
																		id="amcs_analysis_input",
																		value="",
																	),
																],
															),
														],
														md=3
													),
													dbc.Col([
															html.Label("Description"),
															html.Div([
																	html.Div(
																		dbc.Input(
																			id="amcs_description_input",
																			value="",
																		),
																	),
																],
															),
														],
														md=4
													),
													dbc.Col([
															html.Br(),
															html.Div([
																	dbc.Button(
																		"Save", 
																		outline=True, 
																		color="primary",
																		id="amcs_analysis_save_button",
																		style={"width": "100px"}
																	),
																],
																style={"padding-top": "7px"}
															)
														],
														md=2
													),
												]
											),
										],
										style={"border": "1px solid #dee2e6", "padding": "5px"}
									),
									html.Br(),
									html.Label("Find"),
									html.Div([
											dbc.Row([
													dbc.Col([
															html.Label("Database"),
															html.Div([
																	html.Div(
																		dcc.Dropdown(
																			id="amcs_database_dropdown",
																			clearable=False,
																		),
																		style={"width": "90%", "display": "inline-block"}
																	),
																	html.Div(
																		dbc.Button(
																			html.I(className="fas fa-sync"), 
																			outline=True, 
																			color="primary", 
																			id="amcs_database_refresh_button", 
																			style={"height": "36px"}
																		),
																		style={"display": "inline-block", "vertical-align": "top"}
																	),
																],
															)
														],
														md=6
													),
													dbc.Col([
															html.Label("Collection"),
															dcc.Dropdown(
																id="amcs_collection_dropdown",
																clearable=False,
															),
														],
														md=6
													),
												]
											),
											html.Br(),
											dbc.Row([
													dbc.Col([
															html.Label("Find"),
															html.Br(),
															dcc.Input(
																id="amcs_field_input",
																value="{}",
																style={"width": "100%"}
															),
														],
														md=4
													),
													dbc.Col([
															html.Label("Projections"),
															html.Br(),
															dcc.Input(
																id="amcs_projections_input",
																value="{}",
																style={"width": "100%"}
															),
														],
														md=4
													),
													dbc.Col([
															html.Label("Limit"),
															html.Br(),
															dcc.Input(
																id="amcs_limit_input",
																type="number",
																value=100,
																style={"width": "100%"}
															),
														],
														md=2
													),
													dbc.Col([
															html.Label("Skip"),
															html.Br(),
															dcc.Input(
																id="amcs_skip_input",
																type="number",
																value=0,
																style={"width": "100%"}
															),
														],
														md=2
													)
												]
											),
											html.Br(),
											dbc.Button("Filter Data",
												outline=True, 
												color="primary",
												className="mr-1",
												id="amcs_filter_button"
											)
										],
										style={"border": "1px solid #dee2e6", "padding": "5px"}
									),
									html.Br(),
									html.Label("Filter"),
									html.Div([
											dbc.Row([
													dbc.Col([
															html.Label("Category Field"),
															html.Br(),
															dcc.Dropdown(
																id="amcs_category_field_dropdown",
																value=""
															),
														],
														md=3
													),
													dbc.Col([
															html.Label("Event Field"),
															html.Br(),
															dcc.Dropdown(
																id="amcs_event_field_dropdown",
																value=""
															),
														],
														md=3
													),
												]
											),
											html.Br(),
											dbc.Row([
													dbc.Col([
															html.Label("Start Field"),
															html.Br(),
															dcc.Dropdown(
																id="amcs_start_field_dropdown",
																value=""
															),
														],
														md=3
													),
													dbc.Col([
															html.Label("End Field"),
															html.Br(),
															dcc.Dropdown(
																id="amcs_end_field_dropdown",
																value=""
															),
														],
														md=3
													),
													dbc.Col([
															html.Label("Datetime Format"),
															html.Br(),
															dcc.Input(
																id="amcs_datetime_format_field_input",
																value="yyyy-MM-dd"
															),
														],
														md=3
													),
												]
											)
										],
										style={"border": "1px solid #dee2e6", "padding": "5px"}
									),
									html.Br(),
									dbc.Button("Generate Graph",
										outline=True, 
										color="primary",
										className="mr-1",
										id="amcs_generate_button"
									)
								]
							),
							id="amcs_collapse",
							is_open=True
						)
					]
				),
				dbc.Card(
					dbc.CardBody([
							dbc.Tabs([
									dbc.Tab(
										html.Div(
											id="amcs_results_div",
											style={"overflow-y": "scroll", "max-height": "675px"}
										),
										label="Results",
										tab_id="amcs_table"
									),
									dbc.Tab(
										dbc.Textarea(
											id = "amcs_text_area",
											# className="tree",
											style= {"width": "100%", "height": "675px"}

										),
										label="Raw Results",
										tab_id="amcs_raw"
									),
									dbc.Tab(
										html.Div([
												dbc.Row([
														dbc.Col([
																html.Div([], id="amcs_canvas_div", style={"height": "100%", "width": "100%"}),
															],
															style={"height": "675px"},
															md=10
														),
														dbc.Col([
																dbc.Textarea(
																	id="amcs_notes_textarea",
																	className="mb-3",
																	placeholder="Notes...",
																	style={"height": "675px"}
																)
															],
															md=2
														)
													]
												)
											],
										),
										label="Graph",
										tab_id="amcs_graph"
									),
								],
								id="amcs_tabs",
								active_tab="amcs_table",
							)
						]
					),
					style={"height": "750px", "width": "100%"}
				),
			],
			style={"padding-left": "30px", "padding-right": "30px", "padding-top": "30px", "padding-bottom": "30px"}
		)
	],
	id="amcs_component",
	style={"display": "none"}
)

amcd_component = html.Div([
		html.Div([
				html.Label("", id="amcd_data_buffer", hidden=True),
				html.Label("", id="amcd_data_prebuffer", hidden=True),
				html.Label("", id="amcd_output_div", hidden=True),
				html.Label("amcd_canvas_div", id="amcd_div_buffer", hidden=True),

				dbc.Card([
						dbc.CardHeader(
							dbc.Button("Options", outline=True, color="link", id="amcd_collapse_button", style={"height": "100%", "width": "100%"}),
						),
						dbc.Collapse(
							dbc.CardBody([
									html.Label("Analysis"),
									html.Div([
											dbc.Row([
													dbc.Col([
															html.Label("Select Analysis ID"),
															html.Div([
																	html.Div(
																		dcc.Dropdown(
																			id="amcd_analysis_dropdown",
																			clearable=False,
																		),
																	),
																],
															),
														],
														md=3
													),
													dbc.Col([
															html.Label("Analysis ID"),
															html.Div([
																	dbc.Input(
																		id="amcd_analysis_input",
																		value="",
																	),
																],
															),
														],
														md=3
													),
													dbc.Col([
															html.Label("Description"),
															html.Div([
																	html.Div(
																		dbc.Input(
																			id="amcd_description_input",
																			value="",
																		),
																	),
																],
															),
														],
														md=4
													),
													dbc.Col([
															html.Br(),
															html.Div([
																	dbc.Button(
																		"Save", 
																		outline=True, 
																		color="primary",
																		id="amcd_analysis_save_button",
																		style={"width": "100px"}
																	),
																],
																style={"padding-top": "7px"}
															)
														],
														md=2
													),
												]
											),
										],
										style={"border": "1px solid #dee2e6", "padding": "5px"}
									),
									html.Br(),
									html.Label("Find"),
									html.Div([
											dbc.Row([
													dbc.Col([
															html.Label("Database"),
															html.Div([
																	html.Div(
																		dcc.Dropdown(
																			id="amcd_database_dropdown",
																			clearable=False,
																		),
																		style={"width": "90%", "display": "inline-block"}
																	),
																	html.Div(
																		dbc.Button(
																			html.I(className="fas fa-sync"), 
																			outline=True, 
																			color="primary", 
																			id="amcd_database_refresh_button", 
																			style={"height": "36px"}
																		),
																		style={"display": "inline-block", "vertical-align": "top"}
																	),
																],
															)
														],
														md=6
													),
													dbc.Col([
															html.Label("Collection"),
															dcc.Dropdown(
																id="amcd_collection_dropdown",
																clearable=False,
															),
														],
														md=6
													),
												]
											),
											html.Br(),
											dbc.Row([
													dbc.Col([
															html.Label("Find"),
															html.Br(),
															dcc.Input(
																id="amcd_field_input",
																value="{}",
																style={"width": "100%"}
															),
														],
														md=4
													),
													dbc.Col([
															html.Label("Projections"),
															html.Br(),
															dcc.Input(
																id="amcd_projections_input",
																value="{}",
																style={"width": "100%"}
															),
														],
														md=4
													),
													dbc.Col([
															html.Label("Limit"),
															html.Br(),
															dcc.Input(
																id="amcd_limit_input",
																type="number",
																value=100,
																style={"width": "100%"}
															),
														],
														md=2
													),
													dbc.Col([
															html.Label("Skip"),
															html.Br(),
															dcc.Input(
																id="amcd_skip_input",
																type="number",
																value=0,
																style={"width": "100%"}
															),
														],
														md=2
													)
												]
											),
											html.Br(),
											dbc.Button("Filter Data",
												outline=True, 
												color="primary",
												className="mr-1",
												id="amcd_filter_button"
											)
										],
										style={"border": "1px solid #dee2e6", "padding": "5px"}
									),
									html.Br(),
									html.Label("Filter"),
									html.Div([
											dbc.Row([
													dbc.Col([
															html.Label("Category Field"),
															html.Br(),
															dcc.Dropdown(
																id="amcd_category_field_dropdown",
																clearable=False,
															),
														],
														md=3
													),
												]
											),
											html.Br(),
											dbc.Row([
													dbc.Col([
															html.Label("Event Field"),
															html.Br(),
															dcc.Dropdown(
																id="amcd_event_field_dropdown",
																clearable=False,
															),
														],
														md=3
													),
													dbc.Col([
															html.Label("Event Prefix Delimiter"),
															html.Br(),
															dcc.Input(
																id="amcd_event_delimiter_input",
																value=""
															),
														],
														md=3
													)
												]
											),
											html.Br(),
											dbc.Row([
													dbc.Col([
															html.Label("Datetime Field"),
															html.Br(),
															dcc.Dropdown(
																id="amcd_start_field_dropdown",
																clearable=False,
															),
														],
														md=3
													),
													dbc.Col([
															html.Label("Datetime Format"),
															html.Br(),
															dcc.Input(
																id="amcd_datetime_format_field_input",
																value="yyyy-MM-dd HH:mm:ss"
															),
														],
														md=3
													),
												]
											),
										],
										style={"border": "1px solid #dee2e6", "padding": "5px"}
									),
									html.Br(),
									dbc.Button("Generate Graph",
										outline=True, 
										color="primary",
										className="mr-1",
										id="amcd_generate_button"
									)
								]
							),
							id="amcd_collapse",
							is_open=True
						)
					]
				),
				dbc.Card(
					dbc.CardBody([
							dbc.Tabs([
									dbc.Tab(
										html.Div(
											id="amcd_results_div",
											style={"overflow-y": "scroll", "max-height": "675px"}
										),
										label="Results",
										tab_id="amcd_table"
									),
									dbc.Tab(
										dbc.Textarea(
											id = "amcd_text_area",
											# className="tree",
											style= {"width": "100%", "height": "675px"}

										),
										label="Raw Results",
										tab_id="amcd_raw"
									),
									dbc.Tab(
										html.Div([
												dbc.Row([
														dbc.Col([
																html.Label("Date"),
																html.Br(),
																dcc.DatePickerSingle(
																	id="amcd_datepicker",
																	display_format="YYYY-MM-DD",
																),
																html.Div([], id="amcd_canvas_div", style={"height": "100%", "width": "100%"}),
															],
															style={"height": "575px"},
															md=10
														),
														dbc.Col([
																dbc.Textarea(
																	id="amcd_notes_textarea",
																	className="mb-3",
																	placeholder="Notes...",
																	style={"height": "675px"}
																)
															],
															md=2
														)
													],
													style={"height": "750px", "width": "100%"}
												)
											],
										),
										label="Graph",
										tab_id="amcd_graph"
									),
								],
								id="amcd_tabs",
								active_tab="amcd_table",
							)
						]
					),
					style={"height": "750px", "width": "100%"}
				),
			],
			style={"padding-left": "30px", "padding-right": "30px", "padding-top": "30px", "padding-bottom": "30px"}
		)
	],
	id="amcd_component",
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
		dcc.Interval(
			id="interval",
			interval=1*1000, # in milliseconds
			n_intervals=0
		),
		dtc.SideBar([
				dtc.SideBarItem(id="id_1", label="Login", icon="fas fa-sign-in-alt", className="sideBarItem"),
				dtc.SideBarItem(id="id_2", label="Explore", icon="fas fa-compass", className="sideBarItem"),
				dtc.SideBarItem(id="id_3", label="Scoring", icon="fas fa-chart-line", className="sideBarItem"),
				dtc.SideBarItem(id="id_4", label="Custom Graphing", icon="fas fa-chart-bar", className="sideBarItem"),
				dtc.SideBarItem(id="id_5", label="Timeline", icon="fas fa-tasks", className="sideBarItem"),
				dtc.SideBarItem(id="id_6", label="Timeline Daily", icon="fas fa-tasks", className="sideBarItem"),
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
				html.Div([], id="cg_find_toast_div"),
				html.Div([], id="cg_save_toast_div"),
				html.Div([], id="amcs_toast_div"),
				html.Div([], id="amcs_toast_div2"),
				html.Div([], id="amcd_toast_div"),
				html.Div([], id="amcd_toast_div2"),
				html.Div([], id="amcd_save_toast_div"),
				html.Div([], id="amcs_save_toast_div"),

			],
			id="toast_div"
		),
		html.Div([navbar, login_component, explore_component, scoring_component, custom_graphing_component, amcs_component, amcd_component, footer], id="page_content", className="page_content", style={"z-index": "-1"}),
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
		sd = ecosystem_scoring_pdash.ScoringDash(ps_url, ps_username, ps_password, ActiveStates())
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
	return generate_toast("Successfully logged in.", "Success", "success")

@app.callback(
	[
		dash.dependencies.Output("usecase_dropdown", "options"),
		dash.dependencies.Output("usecase_dropdown2", "options"),
	],
	[	
		dash.dependencies.Input("login_status", "children"),
		dash.dependencies.Input("usecase_dropdown", "value"),
		dash.dependencies.Input("usecase_dropdown2", "value"),
		dash.dependencies.Input("usecase_toast_div", "children")
	],
	prevent_initial_call=True)
def callback_login2(children, value, value2, toast):
	try:
		sd.retrieve_properties()
		cl = convert_list(sd.get_use_case_names())
		return cl, cl
	except Exception as e:
		print(e)
		return [], []

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
			return [[]]
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
		field_data = sd.read_field_from_properties(usecase, "predictor.param.lookup")
		return [[]]

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
		acts = sd.get_active_states()
		acts.exp_score_button_busy = True
		acts.exp_score_button_busy_changed = True
		outputs = sd.score_btn_eventhandler(usecase, score_value)
		global graphing_adv_refresh
		graphing_adv_refresh = True
		acts.exp_score_button_busy = False
		acts.exp_score_button_busy_changed = True
		return outputs, []
	except Exception as e:
		print(e)
		return None, generate_toast("Error: Could not score: {}".format(e), "Error", "danger")

@app.callback(
	[
		dash.dependencies.Output("score_button", "children"),
		dash.dependencies.Output("score_button", "disabled")
	],
	[dash.dependencies.Input("interval", "n_intervals")],
	prevent_initial_call=True)
def callback_score_button_busy(intervals):
	try:
		acts = sd.get_active_states()
		if acts.exp_score_button_busy_changed:
			acts.exp_score_button_busy_changed = False
			if acts.score_button_busy:
				return [dbc.Spinner(size="sm"), " Scoring..."], True
			else:
				return "Score", False
		else:
			return dash.no_update, dash.no_update
	except:
		return dash.no_update, dash.no_update

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
def callback_score_buffer(score_b):
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
		return {"width": "98%", "height": "380px", "display": "block"}
	else:
		return {"display": "none"}

@app.callback(
	dash.dependencies.Output("graphing_adv_div", "style"),
	[dash.dependencies.Input("tabs_scoring", "active_tab")],
	prevent_initial_call=True)
def tabs_content_graphing(tab):
	if tab == "graph_adv":
		return {"width": "100%", "display": "block"}
	else:
		return {"display": "none"}

@app.callback(
	dash.dependencies.Output("cg_adv_div", "style"),
	[dash.dependencies.Input("cg_tabs", "active_tab")],
	prevent_initial_call=True)
def tabs_content_custom_graphing(tab):
	if tab == "cg_adv":
		return {"width": "100%", "display": "block"}
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
		return generate_toast("Successfully processed new uploads.", "Success", "success")
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
		return generate_toast("Successfully processed new uploads.", "Success", "success")
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
	if usecase_name == "" or usecase_name == None:
		return generate_toast("Error: No usecase selected.", "Error", "danger")	
	if sd.test_connection(usecase_name):
		return generate_toast("Connection Successful.", "Success", "success")
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
		return generate_toast("Successfully uploaded usecase: {}.".format(usecase_name), "Success", "success")
	except Exception as e:
		print(e)
		return generate_toast("Error: Could not upload usecase: {}.".format(e), "Error", "danger")


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
	[
		dash.dependencies.Output("graphing_adv_div", "children"),
		dash.dependencies.Output("graph_adv_dropdown", "options"),
	],
	[
		dash.dependencies.Input("interval", "n_intervals"),
		dash.dependencies.Input("graph_adv_dropdown", "value"),
	],
	state=[
		State(component_id="score_buffer", component_property="children"),
		State(component_id="graphing_adv_div", component_property="children"),
	],
	prevent_initial_call=True)
def tabs_content_graphing4(interval, dropdown_values, scoring_results, children):
	global graphing_adv_refresh
	if graphing_adv_refresh:
		graphing_adv_refresh = False
		return "Loading", []
	ctx = dash.callback_context
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if dropdown_values == None:
		dropdown_values = []
	if trigger_id == "graph_adv_dropdown":
		graphing_adv_refresh = True
		return dash.no_update, dash.no_update
	if trigger_id == "interval":
		try:
			if children == "Loading":
				jstr = json.loads(scoring_results)
				data_points = []
				for value in jstr:
					flat = json_flatten(value, "")
					data_points.append(flat)
				df = pd.DataFrame(data_points)
				columns = list(df.columns)
				l = [columns]
				l.extend(df.values.tolist())
				return dash_pivottable.PivotTable(
							id="graphing_adv_table",
							data=l,
							cols=["customer"],
							colOrder="key_a_to_z",
							rows=[],
							rowOrder="key_a_to_z",
							rendererName="Line Chart",
							aggregatorName="List Unique Values",
							vals=[],
							unusedOrientationCutoff="Infinity",
							hiddenAttributes=dropdown_values

				), convert_list(columns)
			return dash.no_update, dash.no_update
		except Exception as e:
			print(e)
			return dash.no_update, dash.no_update

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
	if usecase == "" or usecase == None:
		return generate_toast("Error: Could not upload files: Use case is not selected.", "Error", "danger")
	if database == None or database == "":
		return generate_toast("Error: Could not upload files: Database field is empty.", "Error", "danger")
	if (target_fs == None or target_fs == "") and (fs_name != None and fs_name != ""):
		return generate_toast("Error: Could not upload files: Feature Store field is empty.", "Error", "danger")
	if (target_fs != None and target_fs != "") and (fs_name == None or fs_name == ""):
		return generate_toast("Error: Could not upload files: Target Feature Store field is empty.", "Error", "danger")
	if (target_ad == None or target_ad == "") and (ad_name != None and ad_name != ""):
		return generate_toast("Error: Could not upload files: Additional File field is empty.", "Error", "danger")
	if (target_ad != None and target_ad != "") and (ad_name == None or ad_name == ""):
		return generate_toast("Error: Could not upload files: Target Additional File field is empty.", "Error", "danger")

	model_path = tmp_dir + str(model_name)
	fs_path = tmp_dir + str(fs_name)
	ad_path = tmp_dir + str(ad_name)
	try:
		sd.upload_use_case_files(usecase, database, model_path, model_content, fs_path, fs_content, target_fs, ad_path=ad_path, ad_content=ad_content, additional=target_ad)
		return generate_toast("Successfully uploaded files.", "Success", "success")
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
	if predictor == "wellness_score":
		return {"display": "none"}
	if predictor == "spending_personality":
		return {"display": "none"}

	return {"height": "650px"}

@app.callback(
	dash.dependencies.Output("graphing_adv_collapse", "is_open"),
	[
		dash.dependencies.Input("graphing_adv_collapse_button", "n_clicks")
	],
	state=[
		State(component_id="graphing_adv_collapse", component_property="is_open"),
	],
	prevent_initial_call=True
)
def graphing_adv_toggle_collapse(n_clicks, is_open):
	if is_open:
		return False
	return True

@app.callback(
	dash.dependencies.Output("cg_adv_collapse", "is_open"),
	[
		dash.dependencies.Input("cg_adv_collapse_button", "n_clicks")
	],
	state=[
		State(component_id="cg_adv_collapse", component_property="is_open"),
	],
	prevent_initial_call=True
)
def custom_graphing_adv_toggle_collapse(n_clicks, is_open):
	if is_open:
		return False
	return True



# ---- custom graphing ------------------------------------------------------------------------------------------------
@app.callback(
	[
		dash.dependencies.Output("cg_analysis_dropdown", "options"),
		dash.dependencies.Output("cg_analysis_dropdown", "value"),
		dash.dependencies.Output("cg_save_toast_div", "children"),
	],
	[
		dash.dependencies.Input("cg_analysis_save_button", "n_clicks"),
		dash.dependencies.Input("login_status", "children"),		
	],
	state=[
		State(component_id="cg_analysis_input", component_property="value"),
		State(component_id="cg_description_input", component_property="value"),
		State(component_id="cg_database_dropdown", component_property="value"),
		State(component_id="cg_collection_dropdown", component_property="value"),
		State(component_id="cg_field_input", component_property="value"),
		State(component_id="cg_projections_input", component_property="value"),
		State(component_id="cg_limit_input", component_property="value"),
		State(component_id="cg_skip_input", component_property="value"),
		State(component_id="cg_notes_textarea", component_property="value"),
		State(component_id="cg_adv_table_metadata", component_property="cols"),
		State(component_id="cg_adv_table_metadata", component_property="rows"),
		State(component_id="cg_adv_table_metadata", component_property="rendererName"),
		State(component_id="cg_adv_table_metadata", component_property="aggregatorName"),
		State(component_id="cg_adv_table_metadata", component_property="vals"),
		State(component_id="cg_adv_table_metadata", component_property="hiddenAttributes"),
		State(component_id="cg_adv_graph_value_input", component_property="value"),
	],
	prevent_initial_call=True
)

def cg_save_analysis(n_clicks, login_status, name, description, database, collection, field, projections, limit, skip, notes, cols, rows, rendererName, aggregatorName, vals, hiddenAttributes, value):
	try:
		global sd
		a_type = "advanced_graphing"
		ctx = dash.callback_context
		trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
		if trigger_id == "cg_analysis_save_button":
			state = {
				"description": description,
				"database": database,
				"collection": collection,
				"field": field,
				"projections": projections,
				"limit": limit,
				"skip": skip,
				"notes": notes,
				"cols": cols,
				"rows": rows,
				"rendererName": rendererName,
				"aggregatorName": aggregatorName,
				"vals": [value],
				"hiddenAttributes": hiddenAttributes,
			}
			sd.append_graphing_state(name, a_type, state)
			names = sd.get_graphing_state_names(a_type)
			return convert_list(names), name, generate_toast("Success: Saved analysis '{}'.".format(name), "Success", "success")
		names = sd.get_graphing_state_names(a_type)
		return convert_list(names), dash.no_update, []
	except Exception as e:
		print(e)
		return dash.no_update, dash.no_update, dash.no_update

@app.callback(
	[
		dash.dependencies.Output("cg_analysis_input", "value"),
		dash.dependencies.Output("cg_description_input", "value"),
		dash.dependencies.Output("cg_database_dropdown", "value"),
		dash.dependencies.Output("cg_collection_dropdown", "value"),
		dash.dependencies.Output("cg_field_input", "value"),
		dash.dependencies.Output("cg_projections_input", "value"),
		dash.dependencies.Output("cg_limit_input", "value"),
		dash.dependencies.Output("cg_skip_input", "value"),
		dash.dependencies.Output("cg_notes_textarea", "value"),
		dash.dependencies.Output("cg_adv_graph_value_input", "value"),
		dash.dependencies.Output("cg_adv_table_metadata", "cols"),
		dash.dependencies.Output("cg_adv_table_metadata", "rows"),
		dash.dependencies.Output("cg_adv_table_metadata", "rendererName"),
		dash.dependencies.Output("cg_adv_table_metadata", "aggregatorName"),
		dash.dependencies.Output("cg_adv_table_metadata", "vals"),
		dash.dependencies.Output("cg_adv_table_metadata", "hiddenAttributes"),
	],
	[
		dash.dependencies.Input("cg_analysis_dropdown", "value"),
		dash.dependencies.Input("cg_adv_table", "cols"),
		dash.dependencies.Input("cg_adv_table", "rows"),
		dash.dependencies.Input("cg_adv_table", "rendererName"),
		dash.dependencies.Input("cg_adv_table", "aggregatorName"),
		# dash.dependencies.Input("cg_adv_table", "vals"),
		dash.dependencies.Input("cg_adv_table", "hiddenAttributes"),
		# dash.dependencies.Input("cg_adv_table", "valueFilter"),
		dash.dependencies.Input("cg_adv_table", "colOrder"),
		dash.dependencies.Input("cg_adv_table", "rowOrder"),

	],
	state=[
		State(component_id="cg_adv_table", component_property="vals"),
		State(component_id="cg_adv_table", component_property="valueFilter"),
	],
	prevent_initial_call=True
)
def cg_load_analysis(name, cols, rows, rendererName, aggregatorName, hiddenAttributes, colOrder, rowOrder, vals, valueFilter):
	ctx = dash.callback_context
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if trigger_id == "cg_analysis_dropdown":
		global sd
		a_type = "advanced_graphing"
		gstate = sd.get_graphing_state(name, a_type)
		return name, gstate["description"], gstate["database"], gstate["collection"], gstate["field"], gstate["projections"], gstate["limit"], gstate["skip"], gstate["notes"], gstate["vals"][0], gstate["cols"], gstate["rows"], gstate["rendererName"], gstate["aggregatorName"], gstate["vals"], gstate["hiddenAttributes"]
	else:
		return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, cols, rows, rendererName, aggregatorName, vals, hiddenAttributes

@app.callback(
	dash.dependencies.Output("cg_collapse", "is_open"),
	[
		dash.dependencies.Input("cg_collapse_button", "n_clicks")
	],
	state=[
		State(component_id="cg_collapse", component_property="is_open"),
	],
	prevent_initial_call=True
)
def cg_toggle_collapse(n_clicks, is_open):
	if is_open:
		return False
	return True

@app.callback(
	[
		dash.dependencies.Output("cg_collection_dropdown", "options"),
	],
	[	
		dash.dependencies.Input("cg_database_dropdown", "value")
	],
	prevent_initial_call=True)
def callback_database(database):
	try:
		if database == "":
			return [[]]
		collections = sd.get_prediction_collections(database)
		new_collections = []
		for entry in collections["collection"]:
			new_collections.append(entry["name"])
		return [convert_list(new_collections)]
	except Exception as e:
		print(e)
		return [[]]


@app.callback(
	[
		dash.dependencies.Output("cg_database_dropdown", "options"),
	],
	[	
		dash.dependencies.Input("login_status", "children"),
		dash.dependencies.Input("cg_database_refresh_button", "n_clicks")
	],
	prevent_initial_call=True)
def callback_login_cg(children, n_clicks):
	try:
		databases = sd.get_prediction_databases()
		new_databases = []
		for entry in databases["databases"]:
			new_databases.append(entry["name"])
		return [convert_list(new_databases)]
	except Exception as e:
		print(e)
		return [[]]


@app.callback(
	dash.dependencies.Output("cg_text_area", "value"),
	[
		dash.dependencies.Input("cg_find_buffer", "children")
	],
	prevent_initial_call=True)
def callback_find_buffer(find_b):
	try:
		j = json.loads(find_b)
		pj = json.dumps(j, indent=4, sort_keys=True)
		return pj
	except Exception as e:
		print(e)
		return None


@app.callback(
	dash.dependencies.Output("cg_results_div", "children"),
	[dash.dependencies.Input("cg_find_buffer", "children")],
	prevent_initial_call=True)
def tabs_content_results_tab(children):
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
	[
		dash.dependencies.Output("cg_find_buffer", "children"),
		dash.dependencies.Output("cg_find_toast_div", "children")
	],
	[dash.dependencies.Input("cg_find_button", "n_clicks")],
	state=[
		State(component_id="cg_database_dropdown", component_property="value"),
		State(component_id="cg_collection_dropdown", component_property="value"),
		State(component_id="cg_field_input", component_property="value"),
		State(component_id="cg_projections_input", component_property="value"),
		State(component_id="cg_limit_input", component_property="value"),
		State(component_id="cg_skip_input", component_property="value"),
	],
	prevent_initial_call=True)
def callback_find_button(n_clicks, database, collection, field, projections, limit, skip):
	if database == "" or database == None:
		return None, generate_toast("Error: Could not find: Database not selected.", "Error", "danger")
	if collection == "" or collection == None:
		return None, generate_toast("Error: Could not find: Collection not selected.", "Error", "danger")
	try:
		outputs = sd.get_documents(database, collection, field, projections, limit, skip)
		global custom_graphing_adv_refresh
		custom_graphing_adv_refresh = True
		return json.dumps(outputs), []
	except Exception as e:
		print(e)
		return None, generate_toast("Error: Could not find: {}".format(e), "Error", "danger")

@app.callback(
	[
		dash.dependencies.Output("cg_adv_div", "children"),
		dash.dependencies.Output("cg_graph_adv_dropdown", "options"),
	],
	[
		dash.dependencies.Input("interval", "n_intervals"),
		dash.dependencies.Input("cg_graph_adv_dropdown", "value"),
	],
	state=[
		State(component_id="cg_find_buffer", component_property="children"),
		State(component_id="cg_adv_div", component_property="children"),
		State(component_id="cg_adv_table_metadata", component_property="cols"),
		State(component_id="cg_adv_table_metadata", component_property="rows"),
		State(component_id="cg_adv_table_metadata", component_property="rendererName"),
		State(component_id="cg_adv_table_metadata", component_property="aggregatorName"),
		State(component_id="cg_adv_table_metadata", component_property="vals"),
		State(component_id="cg_adv_table_metadata", component_property="hiddenAttributes"),
	],
	prevent_initial_call=True)
def tabs_content_custom_graphing4(interval, dropdown_values, find_results, children, cols, rows, rendererName, aggregatorName, vals, hiddenAttributes):
	global custom_graphing_adv_refresh
	if custom_graphing_adv_refresh:
		custom_graphing_adv_refresh = False
		return "Loading", []
	ctx = dash.callback_context
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if dropdown_values == None:
		dropdown_values = []
	if trigger_id == "cg_graph_adv_dropdown":
		custom_graphing_adv_refresh = True
		return dash.no_update, dash.no_update
	if trigger_id == "interval":
		try:
			if children == "Loading":
				jstr = json.loads(find_results)
				data_points = []
				for value in jstr:
					flat = json_flatten(value, "")
					data_points.append(flat)
				df = pd.DataFrame(data_points)
				columns = list(df.columns)
				l = [columns]
				l.extend(df.values.tolist())
				return dash_pivottable.PivotTable(
							id="cg_adv_table",
							data=l,
							cols=cols,
							colOrder="key_a_to_z",
							rows=rows,
							rowOrder="key_a_to_z",
							rendererName=rendererName,
							aggregatorName=aggregatorName,
							vals=vals,
							unusedOrientationCutoff="Infinity",
							hiddenAttributes=hiddenAttributes

				), convert_list(columns)
			return dash.no_update, dash.no_update
		except Exception as e:
			print(e)
			return dash.no_update, dash.no_update


# ---- amcs -----------------------------------------------------------------------------------------------------------
@app.callback(
	dash.dependencies.Output("amcs_text_area", "value"),
	[
		dash.dependencies.Input("amcs_data_prebuffer", "children")
	],
	prevent_initial_call=True)
def callback_find_buffer(data_buffer):
	try:
		j = json.loads(data_buffer)
		pj = json.dumps(j, indent=4, sort_keys=True)
		return pj
	except Exception as e:
		print(e)
		return None


@app.callback(
	dash.dependencies.Output("amcs_results_div", "children"),
	[
		dash.dependencies.Input("amcs_data_prebuffer", "children")
	],
	prevent_initial_call=True)
def tabs_content_results_tab(data_buffer):
	try:
		jstr = json.loads(data_buffer)
		data_points = []
		for value in jstr:
			flat = json_flatten(value, "")
			data_points.append(flat)
		df = pd.DataFrame(data_points)
		return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
	except Exception as e:
		print(e)
		return None

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
		State(component_id="amcs_datetime_format_field_input", component_property="value"),
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
	[
		dash.dependencies.Output("amcs_analysis_dropdown", "options"),
		dash.dependencies.Output("amcs_analysis_dropdown", "value"),
		dash.dependencies.Output("amcs_save_toast_div", "children"),
	],
	[
		dash.dependencies.Input("amcs_analysis_save_button", "n_clicks"),
		dash.dependencies.Input("login_status", "children"),		
	],
	state=[
		State(component_id="amcs_analysis_input", component_property="value"),
		State(component_id="amcs_description_input", component_property="value"),
		State(component_id="amcs_database_dropdown", component_property="value"),
		State(component_id="amcs_collection_dropdown", component_property="value"),
		State(component_id="amcs_field_input", component_property="value"),
		State(component_id="amcs_projections_input", component_property="value"),
		State(component_id="amcs_limit_input", component_property="value"),
		State(component_id="amcs_skip_input", component_property="value"),
		State(component_id="amcs_category_field_dropdown", component_property="value"),
		State(component_id="amcs_event_field_dropdown", component_property="value"),
		State(component_id="amcs_start_field_dropdown", component_property="value"),
		State(component_id="amcs_end_field_dropdown", component_property="value"),
		State(component_id="amcs_datetime_format_field_input", component_property="value"),
		State(component_id="amcs_notes_textarea", component_property="value"),

	],
	prevent_initial_call=True
)
def amcs_save_analysis(n_clicks, login_status, name, description, database, collection, field, projections, limit, skip, category, event, starttime, endtime, datetime_format, notes):
	try:
		global sd
		a_type = "timeline"
		ctx = dash.callback_context
		trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
		if trigger_id == "amcs_analysis_save_button":
			state = {
				"description": description,
				"database": database,
				"collection": collection,
				"field": field,
				"projections": projections,
				"limit": limit,
				"skip": skip,
				"category": category,
				"event": event,
				"starttime": starttime,
				"endtime": endtime,
				"datetime_format": datetime_format,
				"notes": notes,
			}
			sd.append_graphing_state(name, a_type, state)
			names = sd.get_graphing_state_names(a_type)
			return convert_list(names), name, generate_toast("Success: Saved analysis '{}'.".format(name), "Success", "success")
		names = sd.get_graphing_state_names(a_type)
		return convert_list(names), dash.no_update, []
	except Exception as e:
		print(e)
		return dash.no_update, dash.no_update, dash.no_update

@app.callback(
	[
		dash.dependencies.Output("amcs_analysis_input", "value"),
		dash.dependencies.Output("amcs_description_input", "value"),
		dash.dependencies.Output("amcs_database_dropdown", "value"),
		dash.dependencies.Output("amcs_collection_dropdown", "value"),
		dash.dependencies.Output("amcs_field_input", "value"),
		dash.dependencies.Output("amcs_projections_input", "value"),
		dash.dependencies.Output("amcs_limit_input", "value"),
		dash.dependencies.Output("amcs_skip_input", "value"),
		dash.dependencies.Output("amcs_category_field_dropdown", "value"),
		dash.dependencies.Output("amcs_event_field_dropdown", "value"),
		dash.dependencies.Output("amcs_start_field_dropdown", "value"),
		dash.dependencies.Output("amcs_end_field_dropdown", "value"),
		dash.dependencies.Output("amcs_datetime_format_field_input", "value"),
		dash.dependencies.Output("amcs_notes_textarea", "value"),
	],
	[
		dash.dependencies.Input("amcs_analysis_dropdown", "value")
	],
	prevent_initial_call=True
)
def amcd_load_analysis(name):
	global sd
	a_type = "timeline"
	gstate = sd.get_graphing_state(name, a_type)
	return name, gstate["description"], gstate["database"], gstate["collection"], gstate["field"], gstate["projections"], gstate["limit"], gstate["skip"], gstate["category"], gstate["event"], gstate["starttime"], gstate["endtime"],gstate["datetime_format"],gstate["notes"]


@app.callback(
	[
		dash.dependencies.Output("amcs_database_dropdown", "options"),
	],
	[	
		dash.dependencies.Input("login_status", "children"),
		dash.dependencies.Input("amcs_database_refresh_button", "n_clicks")
	],
	prevent_initial_call=True)
def callback_login_amcs(children, n_clicks):
	try:
		databases = sd.get_prediction_databases()
		new_databases = []
		for entry in databases["databases"]:
			new_databases.append(entry["name"])
		return [convert_list(new_databases)]
	except Exception as e:
		print(e)
		return [[]]



@app.callback(
	[
		dash.dependencies.Output("amcs_collection_dropdown", "options"),
	],
	[	
		dash.dependencies.Input("amcs_database_dropdown", "value")
	],
	prevent_initial_call=True)
def callback_amcs_database(database):
	try:
		if database == "":
			return [[]]
		collections = sd.get_prediction_collections(database)
		new_collections = []
		for entry in collections["collection"]:
			new_collections.append(entry["name"])
		return [convert_list(new_collections)]
	except Exception as e:
		print(e)
		return [[]]

@app.callback(
	[
		dash.dependencies.Output("amcs_category_field_dropdown", "options"),
		dash.dependencies.Output("amcs_event_field_dropdown", "options"),
		dash.dependencies.Output("amcs_start_field_dropdown", "options"),
		dash.dependencies.Output("amcs_end_field_dropdown", "options"),
	],
	[
		dash.dependencies.Input("amcs_data_prebuffer", "children")
	],
	state=[
		State(component_id="amcs_database_dropdown", component_property="value"),
		State(component_id="amcs_collection_dropdown", component_property="value"),
		State(component_id="amcs_field_input", component_property="value"),
		State(component_id="amcs_projections_input", component_property="value"),
		State(component_id="amcs_skip_input", component_property="value"),
	],
	prevent_initial_call=True)
def callback_collection_amcd(data, database, collection, field, projections, skip):
	try:
		results = sd.get_collection_labels(database, collection, field, projections, skip)
		labels = results["labels"][0]
		if "_id" in labels:
			labels.remove("_id")
		converted_labels = convert_list(labels)
		return converted_labels, converted_labels, converted_labels, converted_labels
	except Exception as e:
		print(e)
		return [], [], [], []

@app.callback(
	[
		dash.dependencies.Output("amcs_data_prebuffer", "children"),
		dash.dependencies.Output("amcs_toast_div", "children")
	],
	[dash.dependencies.Input("amcs_filter_button", "n_clicks")],
	state=[
		State(component_id="amcs_database_dropdown", component_property="value"),
		State(component_id="amcs_collection_dropdown", component_property="value"),
		State(component_id="amcs_field_input", component_property="value"),
		State(component_id="amcs_projections_input", component_property="value"),
		State(component_id="amcs_limit_input", component_property="value"),
		State(component_id="amcs_skip_input", component_property="value"),
	],
	prevent_initial_call=True)
def callback_filter_button(n_clicks, database, collection, field, projections, limit, skip):
	if database == "" or database == None:
		return None, generate_toast("Error: Could not find: Database not selected.", "Error", "danger")
	if collection == "" or collection == None:
		return None, generate_toast("Error: Could not find: Collection not selected.", "Error", "danger")
	try:
		acts = sd.get_active_states()
		acts.amcs_filter_button.busy = True
		acts.amcs_filter_button.busy_changed = True
		outputs = sd.get_documents(database, collection, field, projections, limit, skip)
		j_outputs = json.dumps(outputs)
		acts.amcs_filter_button.busy = False
		acts.amcs_filter_button.busy_changed = True
		return j_outputs, []
	except Exception as e:
		print(e)
		return None, generate_toast("Error: Could not filter data: {}".format(e), "Error", "danger")

@app.callback(
	[
		dash.dependencies.Output("amcs_filter_button", "children"),
		dash.dependencies.Output("amcs_filter_button", "disabled")
	],
	[dash.dependencies.Input("interval", "n_intervals")],
	prevent_initial_call=True)
def callback_filter_button_busy(intervals):
	try:
		acts = sd.get_active_states()
		if acts.amcs_filter_button.busy_changed:
			acts.amcs_filter_button.busy_changed = False
			if acts.amcs_filter_button.busy:
				return [dbc.Spinner(size="sm"), " Filtering..."], True
			else:
				return "Filter Data", False
		else:
			return dash.no_update, dash.no_update
	except:
		return dash.no_update, dash.no_update

@app.callback(
	[
		dash.dependencies.Output("amcs_data_buffer", "children"),
		dash.dependencies.Output("amcs_toast_div2", "children")
	],
	[dash.dependencies.Input("amcs_generate_button", "n_clicks")],
	state=[
		State(component_id="amcs_data_prebuffer", component_property="children"),
		State(component_id="amcs_category_field_dropdown", component_property="value"),
		State(component_id="amcs_event_field_dropdown", component_property="value"),
		State(component_id="amcs_start_field_dropdown", component_property="value"),
		State(component_id="amcs_end_field_dropdown", component_property="value"),
	],
	prevent_initial_call=True)
def callback_find_button(n_clicks, data, category_field, event_field, start_field, end_field):
	try:
		acts = sd.get_active_states()
		acts.amcs_generate_button.busy = True
		acts.amcs_generate_button.busy_changed = True
		outputs = json.loads(data)
		formatted_outputs = []
		for output in outputs:
			formatted_document = {
				"category": output[category_field],
				"task": output[event_field],
				"start": output[start_field],
				"end": output[end_field],
			}
			for field in output.keys():
				new_key = "data_{}".format(field)
				formatted_document[new_key] = output[field]
			formatted_outputs.append(formatted_document)
		j_formatted_outputs = json.dumps(formatted_outputs)
		acts.amcs_generate_button.busy = False
		acts.amcs_generate_button.busy_changed = True
		return j_formatted_outputs, []
	except Exception as e:
		print(e)
		return None, generate_toast("Error: Could not find: {}".format(e), "Error", "danger")

@app.callback(
	[
		dash.dependencies.Output("amcs_generate_button", "children"),
		dash.dependencies.Output("amcs_generate_button", "disabled")
	],
	[dash.dependencies.Input("interval", "n_intervals")],
	prevent_initial_call=True)
def callback_filter_button_busy(intervals):
	try:
		acts = sd.get_active_states()
		if acts.amcs_generate_button.busy_changed:
			acts.amcs_generate_button.busy_changed = False
			if acts.amcs_generate_button.busy_busy:
				return [dbc.Spinner(size="sm"), " Generating..."], True
			else:
				return "Generate Graph", False
		else:
			return dash.no_update, dash.no_update
	except:
		return dash.no_update, dash.no_update


# ---- amcd -----------------------------------------------------------------------------------------------------------
@app.callback(
	dash.dependencies.Output("amcd_text_area", "value"),
	[
		dash.dependencies.Input("amcd_data_prebuffer", "children")
	],
	prevent_initial_call=True)
def callback_find_buffer(data_buffer):
	try:
		j = json.loads(data_buffer)
		pj = json.dumps(j, indent=4, sort_keys=True)
		return pj
	except Exception as e:
		print(e)
		return None


@app.callback(
	dash.dependencies.Output("amcd_results_div", "children"),
	[
		dash.dependencies.Input("amcd_data_prebuffer", "children")
	],
	prevent_initial_call=True)
def tabs_content_results_tab(data_buffer):
	try:
		jstr = json.loads(data_buffer)
		data_points = []
		for value in jstr:
			flat = json_flatten(value, "")
			data_points.append(flat)
		df = pd.DataFrame(data_points)
		return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
	except Exception as e:
		print(e)
		return None

app.clientside_callback(
	dash.dependencies.ClientsideFunction(
		namespace="clientside",
		function_name="amcharter_daily"
	),
	dash.dependencies.Output("amcd_output_div", "children"),
	[
		dash.dependencies.Input("amcd_data_buffer", "children"),
		dash.dependencies.Input("amcd_datepicker", "date"),
	],
	state=[
		State(component_id="amcd_div_buffer", component_property="children"),
		State(component_id="amcd_datetime_format_field_input", component_property="value"),
	],
	prevent_initial_call=True)

@app.callback(
	dash.dependencies.Output("amcd_collapse", "is_open"),
	[
		dash.dependencies.Input("amcd_collapse_button", "n_clicks")
	],
	state=[
		State(component_id="amcd_collapse", component_property="is_open"),
	],
	prevent_initial_call=True
)
def amcd_toggle_collapse(n_clicks, is_open):
	if is_open:
		return False
	return True

@app.callback(
	[
		dash.dependencies.Output("amcd_analysis_dropdown", "options"),
		dash.dependencies.Output("amcd_analysis_dropdown", "value"),
		dash.dependencies.Output("amcd_save_toast_div", "children"),
	],
	[
		dash.dependencies.Input("amcd_analysis_save_button", "n_clicks"),
		dash.dependencies.Input("login_status", "children"),		
	],
	state=[
		State(component_id="amcd_analysis_input", component_property="value"),
		State(component_id="amcd_description_input", component_property="value"),
		State(component_id="amcd_database_dropdown", component_property="value"),
		State(component_id="amcd_collection_dropdown", component_property="value"),
		State(component_id="amcd_field_input", component_property="value"),
		State(component_id="amcd_projections_input", component_property="value"),
		State(component_id="amcd_limit_input", component_property="value"),
		State(component_id="amcd_skip_input", component_property="value"),
		State(component_id="amcd_category_field_dropdown", component_property="value"),
		State(component_id="amcd_event_field_dropdown", component_property="value"),
		State(component_id="amcd_event_delimiter_input", component_property="value"),
		State(component_id="amcd_start_field_dropdown", component_property="value"),
		State(component_id="amcd_datetime_format_field_input", component_property="value"),
		State(component_id="amcd_notes_textarea", component_property="value"),
	],
	prevent_initial_call=True
)
def amcd_save_analysis(n_clicks, login_status, name, description, database, collection, field, projections, limit, skip, category, event, event_delimiter, datetime, datetime_format, notes):
	try:
		global sd
		a_type = "timeline_daily"
		ctx = dash.callback_context
		trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
		if trigger_id == "amcd_analysis_save_button":
			state = {
				"description": description,
				"database": database,
				"collection": collection,
				"field": field,
				"projections": projections,
				"limit": limit,
				"skip": skip,
				"category": category,
				"event": event,
				"event_delimiter": event_delimiter,
				"datetime": datetime,
				"datetime_format": datetime_format,
				"notes": notes,
			}
			sd.append_graphing_state(name, a_type, state)
			names = sd.get_graphing_state_names(a_type)
			return convert_list(names), name, generate_toast("Success: Saved analysis '{}'.".format(name), "Success", "success")
		names = sd.get_graphing_state_names(a_type)
		return convert_list(names), dash.no_update, []
	except Exception as e:
		print(e)
		return dash.no_update, dash.no_update, dash.no_update

@app.callback(
	[
		dash.dependencies.Output("amcd_analysis_input", "value"),
		dash.dependencies.Output("amcd_description_input", "value"),
		dash.dependencies.Output("amcd_database_dropdown", "value"),
		dash.dependencies.Output("amcd_collection_dropdown", "value"),
		dash.dependencies.Output("amcd_field_input", "value"),
		dash.dependencies.Output("amcd_projections_input", "value"),
		dash.dependencies.Output("amcd_limit_input", "value"),
		dash.dependencies.Output("amcd_skip_input", "value"),
		dash.dependencies.Output("amcd_category_field_dropdown", "value"),
		dash.dependencies.Output("amcd_event_field_dropdown", "value"),
		dash.dependencies.Output("amcd_event_delimiter_input", "value"),
		dash.dependencies.Output("amcd_start_field_dropdown", "value"),
		dash.dependencies.Output("amcd_datetime_format_field_input", "value"),
		dash.dependencies.Output("amcd_notes_textarea", "value"),
	],
	[
		dash.dependencies.Input("amcd_analysis_dropdown", "value")
	],
	prevent_initial_call=True
)
def amcd_load_analysis(name):
	global sd
	a_type = "timeline_daily"
	gstate = sd.get_graphing_state(name, a_type)
	return name, gstate["description"], gstate["database"], gstate["collection"], gstate["field"], gstate["projections"], gstate["limit"], gstate["skip"], gstate["category"], gstate["event"], gstate["event_delimiter"], gstate["datetime"], gstate["datetime_format"], gstate["notes"]


@app.callback(
	[
		dash.dependencies.Output("amcd_database_dropdown", "options"),
	],
	[	
		dash.dependencies.Input("login_status", "children"),
		dash.dependencies.Input("amcd_database_refresh_button", "n_clicks")
	],
	prevent_initial_call=True)
def callback_login_amcd(children, n_clicks):
	try:
		databases = sd.get_prediction_databases()
		new_databases = []
		for entry in databases["databases"]:
			new_databases.append(entry["name"])
		return [convert_list(new_databases)]
	except Exception as e:
		print(e)
		return [[]]

@app.callback(
	[
		dash.dependencies.Output("amcd_collection_dropdown", "options"),
	],
	[	
		dash.dependencies.Input("amcd_database_dropdown", "value")
	],
	prevent_initial_call=True)
def callback_amcd_database(database):
	try:
		if database == "":
			return [[]]
		collections = sd.get_prediction_collections(database)
		new_collections = []
		for entry in collections["collection"]:
			new_collections.append(entry["name"])
		return [convert_list(new_collections)]
	except Exception as e:
		print(e)
		return [[]]

@app.callback(
	[
		dash.dependencies.Output("amcd_category_field_dropdown", "options"),
		dash.dependencies.Output("amcd_event_field_dropdown", "options"),
		dash.dependencies.Output("amcd_start_field_dropdown", "options"),
	],
	[
		dash.dependencies.Input("amcd_data_prebuffer", "children")
	],
	state=[
		State(component_id="amcd_database_dropdown", component_property="value"),
		State(component_id="amcd_collection_dropdown", component_property="value"),
		State(component_id="amcd_field_input", component_property="value"),
		State(component_id="amcd_projections_input", component_property="value"),
		State(component_id="amcd_skip_input", component_property="value"),
	],
	prevent_initial_call=True)
def callback_collection_amcd(data, database, collection, field, projections, skip):
	try:
		results = sd.get_collection_labels(database, collection, field, projections, skip)
		labels = results["labels"][0]
		if "_id" in labels:
			labels.remove("_id")
		converted_labels = convert_list(labels)
		return converted_labels, converted_labels, converted_labels
	except Exception as e:
		print(e)
		return [], [], []

@app.callback(
	[
		dash.dependencies.Output("amcd_data_prebuffer", "children"),
		dash.dependencies.Output("amcd_toast_div", "children")
	],
	[dash.dependencies.Input("amcd_filter_button", "n_clicks")],
	state=[
		State(component_id="amcd_database_dropdown", component_property="value"),
		State(component_id="amcd_collection_dropdown", component_property="value"),
		State(component_id="amcd_field_input", component_property="value"),
		State(component_id="amcd_projections_input", component_property="value"),
		State(component_id="amcd_limit_input", component_property="value"),
		State(component_id="amcd_skip_input", component_property="value"),
	],
	prevent_initial_call=True)
def callback_filter_button(n_clicks, database, collection, field, projections, limit, skip):
	if database == "" or database == None:
		return None, generate_toast("Error: Could not find: Database not selected.", "Error", "danger")
	if collection == "" or collection == None:
		return None, generate_toast("Error: Could not find: Collection not selected.", "Error", "danger")
	try:
		acts = sd.get_active_states()
		acts.amcd_filter_button.busy = True
		acts.amcd_filter_button.busy_changed = True
		outputs = sd.get_documents(database, collection, field, projections, limit, skip)
		j_outputs = json.dumps(outputs)
		acts.amcd_filter_button.busy = False
		acts.amcd_filter_button.busy_changed = True
		return j_outputs, []
	except Exception as e:
		print(e)
		return None, generate_toast("Error: Could not filter data: {}".format(e), "Error", "danger")


@app.callback(
	[
		dash.dependencies.Output("amcd_filter_button", "children"),
		dash.dependencies.Output("amcd_filter_button", "disabled")
	],
	[dash.dependencies.Input("interval", "n_intervals")],
	prevent_initial_call=True)
def callback_filter_button_busy(intervals):
	try:
		acts = sd.get_active_states()
		if acts.amcd_filter_button.busy_changed:
			acts.amcd_filter_button.busy_changed = False
			if acts.amcd_filter_button.busy:
				return [dbc.Spinner(size="sm"), " Filtering..."], True
			else:
				return "Filter Data", False
		else:
			return dash.no_update, dash.no_update
	except:
		return dash.no_update, dash.no_update


@app.callback(
	[
		dash.dependencies.Output("amcd_data_buffer", "children"),
		dash.dependencies.Output("amcd_datepicker", "date"),
		dash.dependencies.Output("amcd_datepicker", "min_date_allowed"),
		dash.dependencies.Output("amcd_datepicker", "max_date_allowed"),
		dash.dependencies.Output("amcd_toast_div2", "children"),
	],
	[dash.dependencies.Input("amcd_generate_button", "n_clicks")],
	state=[
		State(component_id="amcd_data_prebuffer", component_property="children"),
		State(component_id="amcd_category_field_dropdown", component_property="value"),
		State(component_id="amcd_event_field_dropdown", component_property="value"),
		State(component_id="amcd_event_delimiter_input", component_property="value"),
		State(component_id="amcd_start_field_dropdown", component_property="value"),

	],
	prevent_initial_call=True)
def callback_generate_button(n_clicks, data, category_field, event_field, event_delimiter, start_field):
	try:
		acts = sd.get_active_states()
		acts.amcd_generate_button.busy = True
		acts.amcd_generate_button.busy_changed = True
		prefix_field = "prefix"
		injected_end = "end"
		datetime_field = "start"
		parsed_datetime = "parsed_datetime"
		color_field = "color_index"
		outputs = json.loads(data)
		for output in outputs:
			output[parsed_datetime] = dateutil.parser.parse(output[start_field])
		outputs = sorted(outputs, key = lambda i: i[parsed_datetime])
		first = outputs[0][parsed_datetime]
		last = outputs[-1][parsed_datetime]
		last = last - timedelta(days=1)
		outputs = ecosystem_scoring_pdash.color_by_hour(outputs, parsed_datetime, color_field)
		formatted_outputs = []
		for output in outputs:
			icon = "work"
			if "success" in output[event_field]:
				icon = "dance"
			formatted_document = {
				"category": "",
				"text": output[event_field],
				datetime_field: output[start_field],
				"icon": icon,
				prefix_field: output[event_field].split(event_delimiter)[0],
				color_field: output[color_field]
			}
			formatted_outputs.append(formatted_document)
		formatted_outputs = ecosystem_scoring_pdash.similar_event_timeline(formatted_outputs, prefix_field, datetime_field, injected_end)
		j_formatted_outputs = json.dumps(formatted_outputs)
		acts.amcd_generate_button.busy = False
		acts.amcd_generate_button.busy_changed = True
		return j_formatted_outputs, first, first, last, []
	except Exception as e:
		print(e)
		return None, None, None, None, generate_toast("Error: Could not generate graph: {}".format(e), "Error", "danger")

@app.callback(
	[
		dash.dependencies.Output("amcd_generate_button", "children"),
		dash.dependencies.Output("amcd_generate_button", "disabled")
	],
	[dash.dependencies.Input("interval", "n_intervals")],
	prevent_initial_call=True)
def callback_filter_button_busy(intervals):
	try:
		acts = sd.get_active_states()
		if acts.amcd_generate_button.busy_changed:
			acts.amcd_generate_button.busy_changed = False
			if acts.amcd_generate_button.busy_busy:
				return [dbc.Spinner(size="sm"), " Generating..."], True
			else:
				return "Generate Graph", False
		else:
			return dash.no_update, dash.no_update
	except:
		return dash.no_update, dash.no_update


# ---- Nav-Bar ----------------------------------------------------------------------------------------------------------
@app.callback(
	[
		dash.dependencies.Output("navbar_title", "children"),
	],
	[
		dash.dependencies.Input("navbar_pretitle", "children"),
		dash.dependencies.Input("cg_analysis_dropdown", "value"),
		dash.dependencies.Input("amcs_analysis_dropdown", "value"),
		dash.dependencies.Input("amcd_analysis_dropdown", "value"),
	],
	prevent_initial_call=True)
def update_navbar_title(pretitle, cg, amcs, amcd):
	if pretitle == "Custom Graphing":
		if cg == "" or cg == None:
			return [pretitle]
		return ["{} - {}".format(pretitle, cg)]
	if pretitle == "Timeline":
		if amcs == "" or amcs == None:
			return [pretitle]
		return ["{} - {}".format(pretitle, amcs)]
	if pretitle == "Timeline Daily":
		if amcd == "" or amcd == None:
			return [pretitle]
		return ["{} - {}".format(pretitle, amcd)]
	return [pretitle]

@app.callback(
	[
		dash.dependencies.Output("navbar_pretitle", "children"),
		dash.dependencies.Output("login_component", "style"),
		dash.dependencies.Output("explore_component", "style"),
		dash.dependencies.Output("scoring_component", "style"),
		dash.dependencies.Output("custom_graphing_component", "style"),
		dash.dependencies.Output("amcs_component", "style"),
		dash.dependencies.Output("amcd_component", "style"),
	],
	[
		dash.dependencies.Input("id_1", "n_clicks_timestamp"),
		dash.dependencies.Input("id_2", "n_clicks_timestamp"),
		dash.dependencies.Input("id_3", "n_clicks_timestamp"),
		dash.dependencies.Input("id_4", "n_clicks_timestamp"),
		dash.dependencies.Input("id_5", "n_clicks_timestamp"),
		dash.dependencies.Input("id_6", "n_clicks_timestamp"),
		dash.dependencies.Input("login_status", "children")
	],
)
def toggle_collapse(input1, input2, input3, input4, input5, input6, login_status):
	ctx = dash.callback_context
	y = {"background-color": "#edf1f7", "min-height": "90vh"}
	n = {"display": "none"}
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if trigger_id == "login_status":
		if login_status[:5] == "Error":			
			return "Dashboard",y,n,n,n,n,n
		else:
			return "Explore",n,y,n,n,n,n
	else:
		if len(login_status) <= 2:
			return "Dashboard",y,n,n,n,n,n
		elif login_status[:5] == "Error":
			return "Dashboard",y,n,n,n,n,n
		else:
			if trigger_id == "id_1":
				return "Dashboard",y,n,n,n,n,n

			if trigger_id == "id_2":
				return "Explore",n,y,n,n,n,n

			if trigger_id == "id_3":
				return "Scoring",n,n,y,n,n,n

			if trigger_id == "id_4":
				return "Custom Graphing",n,n,n,y,n,n

			if trigger_id == "id_5":
				return "Timeline",n,n,n,n,y,n

			if trigger_id == "id_6":
				return "Timeline Daily",n,n,n,n,n,y

if __name__ == "__main__":
	app.run_server(debug=True)
