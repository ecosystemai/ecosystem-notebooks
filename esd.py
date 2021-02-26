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
import esd_setup_properties
import json
import base64
import os
# runtime_url = "http://127.0.0.1:8091"
# pred_url = "http://127.0.0.1:4000/api"
# pred_username = "admin@ecosystem.ai"
# pred_password = "password"

sd = None
tmp_dir = "tmp/"
if not os.path.exists(tmp_dir):
	os.mkdir(tmp_dir)

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
	return new_l

app = dash.Dash(__name__)
server = app.server
table_data = [
]
columns = [
]

app.layout = html.Div([
		# Login
		html.Div([
				html.Div([
						html.Div([
								html.Label("Prediction Server URL:", style={"padding-right": "5px"}),
								dcc.Input(
									id="ps_url",
									value="http://127.0.0.1:3001/api",
									# value="",
								),
								html.Label("Prediction Server Username:", style={"padding-left": "15px", "padding-right": "5px"}),
								dcc.Input(
									id="ps_username",
									value="admin@ecosystem.ai",
									# value="",

								),
								html.Label("Prediction Server Password:", style={"padding-left": "15px", "padding-right": "5px"}),
								dcc.Input(
									id="ps_password",
									value="password",
									# value="",
								),
							]
						),
						html.Div([
								html.Label("Runtime Server URL:", style={"padding-right": "5px"}),
								dcc.Input(
									id="rs_url",
									value="http://127.0.0.1:8091",
									# value="",
								),
							]
						)
					]
				),
				html.Div([
						html.Div([
								html.Button("Login",
											id="login_button", 
											type="text",
											style={
												"width": "100%",
												"height": "100%"
											}
								),
							],
							style={"display": "inline-block", "width": "100px", "height": "100%"}
						),
						html.Div([
								html.Div([], id="circle")
							],
							style={"display": "inline-block", "verticalAlign": "bottom", "padding-bottom": "0px", "padding-left": "5px"}
						)
					],
					style={"width": "100%"}
				),
			],
			id="login_div"
		),
		html.Hr(),
		# Filter/Find
		html.Div([
				html.Div([
						html.Label("Use Case"),
						dcc.Dropdown(
							id="usecase_dropdown",
							# options=convert_list(sd.get_use_case_names()),
							clearable=False,
							persistence=True,
							style={"font-size": "13px"}
						),
						html.Label("Find Filter"),
						html.Br(),
						dcc.Input(
							id="find_filter_input",
							value="{}",
							style={"width": "70%"}
						),
						html.Button("Filter",
									id="filter_button", 
									type="text",
									style={
										"width": "26%",
									}
						),
						html.Br(),
						html.Label("Customer"),
						html.Div([
								dcc.RadioItems(
									id="customer_list",
									options = [],
									labelStyle={"display": "block"},
									style={"font-size": "13px"}
								),
							],
							style={"overflow-y": "scroll", "height": "180px", "border": "1px solid grey"}
						)
					],
					style={"display": "inline-block", "verticalAlign": "top", "width": "20%", "height": "300px",}
				),
				html.Div([
						html.Label("Transactions"),
						html.Br(),
						dash_table.DataTable(
							id="datatable",
							columns=columns,
							data=table_data,
							style_header={"backgroundColor": "#3366ff", "color": "white", "font-size": "13px"},
							style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "#f7f9fc"}],
							style_cell={"textAlign": "left", "minWidth": "80px", "font-family": "arial", "font-size": "11px"},
							fixed_rows={'headers': True},
							style_table={"overflowY": "auto", "overflowX": "auto", "height": "280px"},
						)
					],
					style={"display": "inline-block", "float": "right", "width": "78%"}
				)
			],
			# style={"border": "5px solid grey", "width": "100%"}
		),
		# Score/Upload
		html.Div([
				html.Div([
						html.Label("Score Value"),
						html.Br(),
						dcc.Input(
							id="score_value_input",
							value="",
							style={"width": "70%"}
						),
						html.Button("Score",
									id="score_button", 
									type="text",
									style={
										"width": "26%",
									}
						),
						html.Br(),
						html.Br(),
						dcc.Upload(html.Button("Batch Score", style={"width": "98.5%"}), 
							id="batch_score_picker"
						),
						html.Br(),
						html.Hr(),
						html.Div([
								html.Br(),
								html.Label("Customer Data"),
								html.Br(),
								html.Div([
										html.Div([
											dcc.Input(
												id="upload_customer_data",
												value="",
												style={"width": "100%"}
											),
										], style={"display": "inline-block", "width": "85%"}),
										html.Div([
											dcc.Upload(html.Button("..."), id="customer_upload_picker",),
										], style={"display": "inline-block", "padding-left": "8px"})
									]
								),
								html.Button("Upload",
											id="customer_upload_button", 
											type="text",
											style={
												"width": "25%",
											}
								),
								html.Label("Uploaded File.", id="upload_button_label1", hidden=True),
								html.Br(),
								html.Br(),
								html.Label("Transaction Data"),
								html.Br(),
								html.Div([
										html.Div([
											dcc.Input(
												id="upload_transaction_data",
												value="",
												style={"width": "100%"}
											),
										], style={"display": "inline-block", "width": "85%"}),
										html.Div([
											dcc.Upload(html.Button("..."), id="transaction_upload_picker",),
										], style={"display": "inline-block", "padding-left": "8px"})
									]
								),
								html.Button("Upload",
											id="transaction_upload_button", 
											type="text",
											style={
												"width": "25%",
											}
								),
								html.Label("Uploaded File.", id="upload_button_label2", hidden=True),
								html.Br(),
								html.Br(),
								html.Label("CTO Data"),
								html.Br(),
								html.Div([
										html.Div([
											dcc.Input(
												id="upload_cto_data",
												value="",
												style={"width": "100%"}
											),
										], style={"display": "inline-block", "width": "85%"}),
										html.Div([
											dcc.Upload(html.Button("..."), id="cto_upload_picker",),
										], style={"display": "inline-block", "padding-left": "8px"})
									]
								),
								html.Button("Upload",
											id="cto_upload_button", 
											type="text",
											style={
												"width": "25%",
											}
								),
								html.Label("Uploaded File.", id="upload_button_label3", hidden=True),
								html.Br(),
								html.Br(),
								html.Div([
										html.Div([
												html.Button("Process Uploads",
															id="process_uploads_button", 
															type="text",
															style={
																"width": "100%"
															}
												),
											],
											style={"display": "inline-block", "width": "88%", "height": "100%"}
										),
										html.Div([
												html.Div([], id="circle2")
											],
											style={"display": "inline-block", "verticalAlign": "bottom", "padding-bottom": "0x", "padding-left": "5px"}
										)
									],
									style={"width": "100%"}
								),
							],
							id = "upload_div",
							style= {"width": "98%", "height": "380px"}
						)
					],
					style={"display": "inline-block", "verticalAlign": "top", "width": "20%", "height": "300px",}
				),
				html.Div([
						html.Label("Scoring Output"),
						html.Br(),
						dcc.Tabs(id="tabs_scoring", value="scoring", parent_className="custom-tabs",
							children=[
								dcc.Tab(label="Scoring Raw", value="scoring"),
								dcc.Tab(label="Scoring", value="scoring_tab"),
								dcc.Tab(label="Graph", value="graph"),
							],
						),
						html.Div([
								dash_table.DataTable(
									id="scoring_datatable",
									columns=[],
									data=[],
									style_header={"backgroundColor": "#3366ff", "color": "white", "font-size": "13px"},
									style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "#f7f9fc"}],
									style_cell={"textAlign": "left", "minWidth": "250px", "whiteSpace": "normal", "height": "auto", "font-family": "arial", "font-size": "11px"},
									fixed_rows={'headers': True},
									style_table={"overflowY": "auto", "overflowX": "auto", "height": "380px", "display": "none"},
								),
								dcc.Textarea(
									id = "scoring_text_area",
									value = "",
									style= {"width": "98%", "height": "380px"}
								),
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
									style= {"width": "98%", "height": "380px", "display": "none"}
								),
							],
						)
					],
					style={"display": "inline-block", "float": "right", "width": "78%"}
				)
			],
			# style={"border": "5px solid grey", "width": "100%"}
		)
	],
	id="full_div"
)

@app.callback(
	dash.dependencies.Output("circle", "style"),
	[dash.dependencies.Input("login_button", "n_clicks")],
	state=[
		State(component_id="ps_url", component_property="value"),
		State(component_id="ps_username", component_property="value"),
		State(component_id="ps_password", component_property="value"),
		State(component_id="rs_url", component_property="value"),
	],
	prevent_initial_call=True)
def callback_login(clicks, ps_url, ps_username, ps_password, rs_url):
	global sd
	try:
		sd = ecosystem_scoring_pdash.ScoringDash(rs_url, ps_url, ps_username, ps_password)
	except:
		sd = None
		return {"background": "red"}
	return {"background": "#00d68f"}


@app.callback(
	dash.dependencies.Output("usecase_dropdown", "options"),
	[dash.dependencies.Input("circle", "style")],
	prevent_initial_call=True)
def callback_login2(style):
	esd_setup_properties.setup(sd)
	return convert_list(sd.get_use_case_names())

@app.callback(
	dash.dependencies.Output("datatable", "columns"),
	[dash.dependencies.Input("customer_list", "value")],
	state=[
		State(component_id="usecase_dropdown", component_property="value"),
	],
	prevent_initial_call=True)
def callback_customer_list_header(customer, usecase):
	data = sd.dropdown_customer_header_eventhandler(customer, usecase)
	return data

@app.callback(
	dash.dependencies.Output("datatable", "data"),
	[dash.dependencies.Input("customer_list", "value")],
	state=[
		State(component_id="usecase_dropdown", component_property="value"),
	],
	prevent_initial_call=True)
def callback_customer_list(customer, usecase):
	data = sd.dropdown_customer_eventhandler(customer, usecase)
	return data

# Buttons
@app.callback(
	dash.dependencies.Output("customer_list", "options"),
	[dash.dependencies.Input("filter_button", "n_clicks")],
	state=[
		State(component_id="usecase_dropdown", component_property="value"),
		State(component_id="find_filter_input", component_property="value"),
	],
	prevent_initial_call=True)
def callback_find_filter_button(n_clicks, usecase, find_filter):
	opts = sd.find_btn_eventhandler(usecase, find_filter)
	return opts

@app.callback(
	dash.dependencies.Output("scoring_text_area", "value"),
	[dash.dependencies.Input("score_button", "n_clicks")],
	state=[
		State(component_id="usecase_dropdown", component_property="value"),
		State(component_id="score_value_input", component_property="value"),
	],
	prevent_initial_call=True)
def callback_score_button(n_clicks, usecase, score_value):
	outputs = sd.score_btn_eventhandler(usecase, score_value)
	return outputs

@app.callback(
	dash.dependencies.Output("tabs_scoring", "value"),
	[dash.dependencies.Input("score_button", "n_clicks")],
	prevent_initial_call=True)
def callback_score_button(n_clicks):
	return "scoring"

@app.callback(
	dash.dependencies.Output("scoring_text_area", "style"),
	[dash.dependencies.Input("tabs_scoring", "value")],
	prevent_initial_call=True)
def tabs_content_scoring(tab):
	if tab == "scoring":
		return {"display": "block", "width": "100%", "height": "380px"}
	else:
		return {"display": "none"}

@app.callback(
	dash.dependencies.Output("scoring_datatable", "style_table"),
	[dash.dependencies.Input("tabs_scoring", "value")],
	prevent_initial_call=True)
def tabs_content_scoring_tab(tab):
	if tab == "scoring_tab":
		return {"overflowY": "auto", "overflowX": "auto", "height": "380px", "display": "block"},
	else:
		return {"display": "none"}

@app.callback(
	dash.dependencies.Output("scoring_datatable", "columns"),
	[dash.dependencies.Input("tabs_scoring", "value")],
	state=[
		State(component_id="scoring_text_area", component_property="value"),
	],
	prevent_initial_call=True)
def tabs_content_scoring_tab3(tab, scoring_results):
	jstr = json.loads(scoring_results)
	flat = json_flatten(jstr[0], "")
	columns = []
	for key in flat.keys():
		value = {
			"name": key,
			"id": key
		}
		columns.append(value)
	return columns

@app.callback(
	dash.dependencies.Output("scoring_datatable", "data"),
	[dash.dependencies.Input("tabs_scoring", "value")],
	state=[
		State(component_id="scoring_text_area", component_property="value"),
	],
	prevent_initial_call=True)
def tabs_content_scoring_tab2(tab, scoring_results):
	jstr = json.loads(scoring_results)
	data_points = []
	for value in jstr:
		flat = json_flatten(value, "")
		data_points.append(flat)
	return data_points


@app.callback(
	dash.dependencies.Output("score_value_input", "value"),
	[dash.dependencies.Input("batch_score_picker", "contents")],
	prevent_initial_call=True)
def batch_uploader(contents):
	content_type, content_string = contents.split(',')
	decoded = base64.b64decode(content_string)
	text = decoded.decode("utf-8")
	custs = text.split("\n")
	return ",".join(custs)

@app.callback(
	dash.dependencies.Output("graphing_div", "style"),
	[dash.dependencies.Input("tabs_scoring", "value")],
	prevent_initial_call=True)
def tabs_content_graphing(tab):
	if tab == "graph":
		style= {"width": "98%", "height": "380px", "display": "block"}
	else:
		return {"display": "none"}


@app.callback(
	dash.dependencies.Output("graph_dropdown", "options"),
	[dash.dependencies.Input("tabs_scoring", "value")],
	state=[
		State(component_id="scoring_text_area", component_property="value"),
	],
	prevent_initial_call=True)
def tabs_content_graphing2(tab, scoring_results):
	jstr = json.loads(scoring_results)
	value = jstr[0]
	flat = json_flatten(value, "")
	l = list(flat.keys())
	return convert_list(l)

@app.callback(
	dash.dependencies.Output("graphing", "figure"),
	[dash.dependencies.Input("graph_dropdown", "value")],
	state=[
		State(component_id="scoring_text_area", component_property="value"),
	],
	prevent_initial_call=True)
def tabs_content_graphing3(graph_dropdown_value, scoring_results):
	jstr = json.loads(scoring_results)
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
	dash.dependencies.Output("upload_customer_data", "value"),
	[dash.dependencies.Input("customer_upload_picker", "contents")],
	state=[
		State(component_id="customer_upload_picker", component_property="filename"),
	],
	prevent_initial_call=True)
def upload_prep_customers(contents, filename):
	return filename

@app.callback(
	dash.dependencies.Output("upload_transaction_data", "value"),
	[dash.dependencies.Input("transaction_upload_picker", "contents")],
	state=[
		State(component_id="transaction_upload_picker", component_property="filename"),
	],
	prevent_initial_call=True)
def upload_prep_transactions(contents, filename):
	return filename

@app.callback(
	dash.dependencies.Output("upload_cto_data", "value"),
	[dash.dependencies.Input("cto_upload_picker", "contents")],
	state=[
		State(component_id="cto_upload_picker", component_property="filename"),
	],
	prevent_initial_call=True)
def upload_prep_cto(contents, filename):
	return filename

@app.callback(
	dash.dependencies.Output("upload_button_label1", "hidden"),
	[dash.dependencies.Input("customer_upload_button", "n_clicks")],
	state=[
		State(component_id="customer_upload_picker", component_property="filename"),
		State(component_id="customer_upload_picker", component_property="contents"),
	],
	prevent_initial_call=True)
def upload_file_customers(n_clicks, filename, contents):
	sd.upload_btn_eventhandler(tmp_dir, filename, contents)
	return False

@app.callback(
	dash.dependencies.Output("upload_button_label2", "hidden"),
	[dash.dependencies.Input("transaction_upload_button", "n_clicks")],
	state=[
		State(component_id="transaction_upload_picker", component_property="filename"),
		State(component_id="transaction_upload_picker", component_property="contents"),
	],
	prevent_initial_call=True)
def upload_file_transactions(n_clicks, filename, contents):
	sd.upload_btn_eventhandler2(tmp_dir, filename, contents)
	return False

@app.callback(
	dash.dependencies.Output("upload_button_label3", "hidden"),
	[dash.dependencies.Input("cto_upload_button", "n_clicks")],
	state=[
		State(component_id="cto_upload_picker", component_property="filename"),
		State(component_id="cto_upload_picker", component_property="contents"),
	],
	prevent_initial_call=True)
def upload_file_cto(n_clicks, filename, contents):
	sd.upload_btn_eventhandler3(tmp_dir, filename, contents)
	return False


@app.callback(
	dash.dependencies.Output("circle2", "style"),
	[dash.dependencies.Input("process_uploads_button", "n_clicks")],
	state=[
		State(component_id="usecase_dropdown", component_property="value"),
	],
	prevent_initial_call=True)
def callback_process_uploads(clicks, usecase):
	# try:
	sd.process_upload_btn_eventhandler(usecase, tmp_dir + "to_upload.csv")
	# except:
	# 	return {"background": "red"}
	return {"background": "#00d68f"}

if __name__ == "__main__":
	app.run_server(debug=True)
