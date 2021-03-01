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
import dash_bootstrap_components as dbc

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
				html.Button("Login", id="accordion_button", className="accordion"),
				html.Div([
						html.Div([
								html.Div([
										html.Label("Prediction Server URL:", style={"padding-right": "5px"}),
										dcc.Input(
											id="ps_url",
											style={"background-color": "white"},
											value="http://127.0.0.1:3001/api",
											# value="",
										),
									]
								),
								html.Div([
										html.Label("Prediction Server Username:", style={"padding-right": "5px"}),
										dcc.Input(
											id="ps_username",
											style={"background-color": "white"},
											value="admin@ecosystem.ai",
											# value="",
										),
									]
								),
								html.Div([
										html.Label("Prediction Server Password:", style={"padding-right": "5px"}),
										dcc.Input(
											id="ps_password",
											style={"background-color": "white"},
											value="password",
											# value="",
										),
									]
								),
								html.Div([
										html.Label("Runtime Server URL:", style={"padding-right": "5px"}),
										dcc.Input(
											id="rs_url",
											style={"background-color": "white"},
											value="http://127.0.0.1:8091",
											# value="",
										),
									]
								)
							],
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
										html.Label("", id="login_status", style={"font-size": "11px"})
									],
									style={"display": "inline-block", "verticalAlign": "bottom", "padding-bottom": "4px", "padding-left": "5px"}
								)
							],
							style={"width": "100%"}
						),
					],
					id="login_div",
					className="login_off"
				),
			],
			style={"width": "26%"}
		),
		html.Hr(),
		# Filter/Find
		html.Div([
				html.Div([
						html.H3("Use Case Details:"),
						html.Label("Use Case"),
						dcc.Dropdown(
							id="usecase_dropdown",
							# options=convert_list(sd.get_use_case_names()),
							clearable=False,
							persistence=True,
							style={"font-size": "13px"}
						),
						html.Br(),
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
						),
						html.Div([
							html.Br(),
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
							dcc.Upload(html.Button("Batch Score", style={"width": "35%"}), 
								id="batch_score_picker"
							),
							html.Br()
						],
						style={"width": "100%"}
					),
					],
					style={"display": "inline-block", "verticalAlign": "top", "width": "20%", "height": "470px",}
				),
				html.Div([
						html.H3("Transaction Details:"),
						dash_table.DataTable(
							id="datatable",
							columns=columns,
							data=table_data,
							style_header={"backgroundColor": "#3366ff", "color": "white", "font-size": "13px"},
							style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "#f7f9fc"}],
							style_cell={"textAlign": "left", "minWidth": "80px", "font-family": "arial", "font-size": "11px"},
							fixed_rows={"headers": True},
							style_table={"overflowY": "auto", "overflowX": "auto", "height": "280px"},
						)
					],
					style={"display": "inline-block", "width": "58%", "padding-left": "20px"}
				),
				html.Div([
						html.H3("Upload Data:"),
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
						html.Br(),
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
						html.Br(),
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
						html.Br(),
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
									style={"display": "inline-block", "width": "35%", "height": "100%"}
								),
								html.Div([
										html.Label("", id="upload_status", style={"font-size": "11px"})
									],
									style={"display": "inline-block", "verticalAlign": "bottom", "padding-bottom": "11px", "padding-left": "5px"}
								)
							],
							style={"width": "100%"}
						),
					],
					id = "upload_div",
					style= {"display": "inline-block", "float": "right", "width": "20%"}
				)
			],
			# style={"border": "5px solid grey", "width": "100%"}
		),
		html.Hr(),
		html.Div([
				html.Div([
						html.H3("Scoring Output"),
						dcc.Tabs(id="tabs_scoring", value="scoring", parent_className="custom-tabs",
							children=[
								dcc.Tab(label="Scoring Raw", value="scoring"),
								dcc.Tab(label="Scoring", value="scoring_tab"),
								dcc.Tab(label="Graph", value="graph"),
							],
						),
						html.Div([
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
											style= {"width": "100%", "height": "380px"}
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
											style= {"width": "100%", "height": "380px", "display": "none"}
										),
									],
									style= {"width": "100%", "height": "380px"}
								)
							],
						)
					],
					style={"width": "100%"}
				)
			],
			# style={"border": "5px solid grey", "width": "100%"}
		)
	],
	id="full_div"
)

@app.callback(
	dash.dependencies.Output("login_div", "className"),
	[dash.dependencies.Input("accordion_button", "n_clicks")],
	state=[
		State(component_id="login_div", component_property="className"),
	],
	prevent_initial_call=True)
def callback_login_accordion(clicks, className):
	if className == "login_off":
		return "login_on"
	return "login_off"

@app.callback(
	dash.dependencies.Output("accordion_button", "className"),
	[dash.dependencies.Input("accordion_button", "n_clicks")],
	state=[
		State(component_id="accordion_button", component_property="className"),
	],
	prevent_initial_call=True)
def callback_login_accordion2(clicks, className):
	if className == "accordion_active":
		return "accordion"
	return "accordion_active"

@app.callback(
	dash.dependencies.Output("login_status", "children"),
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
		return "Error: Could not log in."
	return "Successfully logged in."


@app.callback(
	dash.dependencies.Output("usecase_dropdown", "options"),
	[dash.dependencies.Input("login_status", "children")],
	prevent_initial_call=True)
def callback_login2(children):
	if children[:5] == "Error":
		return {}
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
	[
		dash.dependencies.Input("batch_score_picker", "contents"),
		dash.dependencies.Input("customer_list", "value")
	],
	state=[
		State(component_id="score_value_input", component_property="value"),
	],
	prevent_initial_call=True)
def batch_uploader(contents, list_value, input_contents):
	ctx = dash.callback_context
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if trigger_id == "batch_score_picker":
		content_type, content_string = contents.split(",")
		decoded = base64.b64decode(content_string)
		text = decoded.decode("utf-8")
		custs = text.split("\n")
		return ",".join(custs)
	if trigger_id == "customer_list":
		if input_contents != "":
			l = input_contents.split(",")
			l.append(list_value)
			return ",".join(l)
		else:
			return list_value

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
	dash.dependencies.Output("upload_status", "children"),
	[dash.dependencies.Input("process_uploads_button", "n_clicks")],
	state=[
		State(component_id="usecase_dropdown", component_property="value"),
	],
	prevent_initial_call=True)
def callback_process_uploads(clicks, usecase):
	try:
		sd.process_upload_btn_eventhandler(usecase, tmp_dir + "to_upload.csv")
	except:
		return "Error: Processing uploads failed"
	return "Uploads successfully uploaded"

if __name__ == "__main__":
	app.run_server(debug=True)
