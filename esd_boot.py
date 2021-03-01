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
import pandas as pd
import dash_bootstrap_components as dbc
import dash_trich_components as dtc


ECO_LOGO = "./assets/favicon.ico"

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

# app = dash.Dash(__name__)
# BOOTSTRAP,GRID,CERULEAN,COSMO,CYBORG,DARKLY,FLATLY,JOURNAL,LITERA,LUMEN,LUX,MATERIA,MINTY,PULSE,SANDSTONE,SIMPLEX,SKETCHY,SLATE,SOLAR,SPACELAB,SUPERHERO,UNITED,YETI
external_scripts = []
external_stylesheets = [dbc.themes.GRID, "https://use.fontawesome.com/releases/v5.15.1/css/all.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
table_data = [
]
columns = [
]
scoring_output = ""

# tools = dbc.Row([
# 		dbc.Col(
# 			dbc.NavItem(dbc.NavLink("Page 1", href="#")),
# 		),
# 		dbc.Col(
# 			dbc.DropdownMenu(
# 				children=[
# 					dbc.DropdownMenuItem("More pages", header=True),
# 					dbc.DropdownMenuItem("Page 2", href="#"),
# 					dbc.DropdownMenuItem("Page 3", href="#"),
# 				],
# 				nav=True,
# 				in_navbar=True,
# 				label="More",
# 			)
# 		)
# 	],
# 	align="center",
# 	no_gutters=True,
# 	className="ml-auto flex-nowrap mt-3 mt-md-0",
# )
#343a40
navbar = dbc.Navbar([
		# Use row and col to control vertical alignment of logo / brand
		dbc.Row(
			[
				dbc.Col(html.Img(src=ECO_LOGO, height="30px"), md=1),
				dbc.Col(dbc.NavbarBrand("Ecosystem.AI Runtime Scoring Dashboard", className="ml-2")),
			],
			align="center",
			no_gutters=True,
		),
	],
	color="dark",
	dark=True,
	sticky="top",
)





login_component = html.Div([
		navbar,
		html.Div([
				dbc.Card(
					dbc.CardBody([
							html.H3("Login Details:", className="card-title"),
							dbc.Form(
								[
									dbc.FormGroup(
										[
											dbc.Label("Prediction Server URL"),
											dbc.Input(
												# placeholder="Enter Prediction Server URL", 
												id="ps_url",
												type="text",
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
												value="admin@ecosystem.ai"
											),
										]
									),
									dbc.FormGroup(
										[
											dbc.Label("Prediction Server Password"),
											dbc.Input(
												# placeholder="Enter Prediction Server Password", 
												id="ps_password",
												type="text",
												value="password"
											),
										]
									),
									dbc.FormGroup(
										[
											dbc.Label("Runtime Server URL"),
											dbc.Input(
												# placeholder="Enter Runtime Server URL",
												id="rs_url",
												type="text",
												value="http://127.0.0.1:8091"
											),
										]
									),
								]
							),
							dbc.Button("Login", id="login_button", color="primary", className="mr-1"),
							html.Label("", id="login_status", style={"display": "none"}),
							html.Div([], id="login_alert_box")
						]
					)
				)
			],
			style={"padding-left": "10px", "padding-right": "10px", "padding-top": "10px"}
		)
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
												html.H3("Use Case Details:", className="card-title"),
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
												dbc.InputGroup(
													[
														dcc.Input(
															id="find_filter_input",
															value="{}"
														),
														dbc.InputGroupAddon(
															dbc.Button("Filter", color="primary", id="filter_button"),
															addon_type="append",
														),
													]
												),
												html.Br(),
												html.Label("Customer"),
												html.Div([
														dbc.RadioItems(
															id="customer_list",
															options = []
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
															dbc.Button("Score", color="primary", id="score_button"),
															addon_type="append",
														),
													]
												),
												html.Br(),
												dcc.Upload(
													dbc.Button("Batch Score", color="primary", className="mr-1"),
													id="batch_score_picker"
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
												html.Div([
														html.H3("Transaction Details:", className="card-title"),
														html.Div([
																dbc.ListGroup([], id="table_div", style={"overflow-y": "scroll", "max-height": "500px"})
															],
														)
													],
													style={"height": "598px"}
												)
												# dash_table.DataTable(
												# 	id="datatable",
												# 	columns=columns,
												# 	data=table_data,
												# 	style_header={"backgroundColor": "#3366ff", "color": "white", "font-size": "13px"},
												# 	style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "#f7f9fc"}],
												# 	style_cell={"textAlign": "left", "minWidth": "80px", "font-family": "arial", "font-size": "11px"},
												# 	fixed_rows={"headers": True},
												# 	style_table={"overflowY": "auto", "overflowX": "auto", "height": "280px"},
												# )
											]
										)
									)
								],
								# style={"border": "5px solid grey", "width": "100%"}
							),
							md=6
						),
						dbc.Col(
							html.Div(
								[
									dbc.Card(
										dbc.CardBody(
											html.Div([
													html.H3("Upload Data:", className="card-title"),
													html.Label("Customer Data"),
													html.Br(),
													dbc.InputGroup(
														[
															dcc.Input(
																id="upload_customer_data"
															),
															dbc.InputGroupAddon(
																dcc.Upload(dbc.Button(html.I(className="fas fa-upload"), color="primary"), id="customer_upload_picker",),
																addon_type="append",
															),
														]
													),
													html.Br(),
													dbc.Button("Upload", 
														color="primary",
														className="mr-1",
														id="customer_upload_button"
													),
													html.Label("Uploaded File.", id="upload_button_label1", hidden=True),
													html.Br(),
													html.Br(),
													html.Label("Transaction Data"),
													html.Br(),
													dbc.InputGroup(
														[
															dcc.Input(
																id="upload_transaction_data"
															),
															dbc.InputGroupAddon(
																dcc.Upload(dbc.Button(html.I(className="fas fa-upload"), color="primary"), id="transaction_upload_picker",),
																addon_type="append",
															),
														]
													),
													html.Br(),
													dbc.Button("Upload", 
														color="primary",
														className="mr-1",
														id="transaction_upload_button"
													),
													html.Label("Uploaded File.", id="upload_button_label2", hidden=True),
													html.Br(),
													html.Br(),
													html.Label("CTO Data"),
													html.Br(),
													dbc.InputGroup(
														[
															dcc.Input(
																id="upload_cto_data"
															),
															dbc.InputGroupAddon(
																dcc.Upload(dbc.Button(html.I(className="fas fa-upload"), color="primary"), id="cto_upload_picker",),
																addon_type="append",
															),
														]
													),
													html.Br(),
													dbc.Button("Upload", 
														color="primary",
														className="mr-1",
														id="cto_upload_button"
													),
													html.Label("Uploaded File.", id="upload_button_label3", hidden=True),
													html.Br(),
													html.Br(),
													dbc.Button("Process Uploads", 
														color="primary",
														className="mr-1",
														id="process_uploads_button"
													),				
													html.Label("", id="upload_status")
												],
												style={"height": "598px"}
											)
										)
									)
								],
								# style={"border": "5px solid grey", "width": "100%"}
							),
							md=3
						)
					],
				),
				html.Br(),
				html.Div([
						html.Div(
							dbc.Card(
								dbc.CardBody([
										html.H3("Scoring Output", className="card-title"),
										dbc.Tabs([
												dbc.Tab(
													html.Div([],
														id = "scoring_text_area",
														className="tree",
														style= {"width": "100%", "height": "495px"}
													),
													label="Scoring Raw",
													tab_id="scoring"
												),
												dbc.Tab(
													html.Div(
														dash_table.DataTable(
															id="scoring_datatable",
															columns=[],
															data=[],
															style_header={"backgroundColor": "#3366ff", "color": "white", "font-size": "13px"},
															style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "#f7f9fc"}],
															style_cell={"textAlign": "left", "minWidth": "250px", "whiteSpace": "normal", "height": "auto", "font-family": "arial", "font-size": "11px"},
															fixed_rows={"headers": True},
															style_table={"overflowY": "auto", "overflowX": "auto", "height": "580px"},
															
														)
													),
													label="Scoring",
													tab_id="scoring_table"
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
											],
											id="tabs_scoring",
											active_tab="scoring",
										)
									]
								)
							)
							# style={"width": "100%"}
						)
					],
					# style={"border": "5px solid grey", "width": "100%"}
				)
			],
			style={"padding-left": "10px", "padding-right": "10px", "padding-top": "10px"}
		)
	],
	id="scoring_component",
	style={"display": "none"}
)

app.layout = html.Div([
		dtc.SideBar([
				dtc.SideBarItem(id="id_1", label="Login", icon="fas fa-sign-in-alt"),
				dtc.SideBarItem(id="id_2", label="Scoring", icon="fas fa-chart-line")
			],
			bg_color="#343a40"
			# bg_color="#1144dd"
		),
		html.Div([login_component, scoring_component], id="page_content", className="page_content"),
	], 
	style={"position": "relative"}
)

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
	dash.dependencies.Output("login_alert_box", "children"),
	[dash.dependencies.Input("login_status", "children")],
	prevent_initial_call=True)
def callback_login3(children):
	if children[:5] == "Error":
		return dbc.Alert("Error: Could not log in.", color="danger")
	return dbc.Alert("Successfully logged in.", color="primary")

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
	dash.dependencies.Output("table_div", "children"),
	[dash.dependencies.Input("customer_list", "value")],
	state=[
		State(component_id="usecase_dropdown", component_property="value"),
	],
	prevent_initial_call=True)
def callback_customer_list(customer, usecase):
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
	dash.dependencies.Output("scoring_text_area", "children"),
	[dash.dependencies.Input("score_button", "n_clicks")],
	state=[
		State(component_id="usecase_dropdown", component_property="value"),
		State(component_id="score_value_input", component_property="value"),
	],
	prevent_initial_call=True)
def callback_score_button(n_clicks, usecase, score_value):
	global scoring_output
	outputs_text = sd.score_btn_eventhandler(usecase, score_value)
	scoring_output = outputs_text
	outputs = html.Div([
			html.Script("""
				const data ='[{"field1": "hello","field2": "bye","customer": 1},{"field1": "hello1","field2": "bye1","customer": 2},{"field1": "hello2","field2": "bye2","customer": 3}]';
				const tree = JsonView.createTree();
				JsonView.render(tree, document.querySelector('.tree'));
				JsonView.expandChildren(tree);
			""")
		]
	)
	return outputs

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
	[dash.dependencies.Input("tabs_scoring", "active_tab")],
	prevent_initial_call=True)
def tabs_content_graphing(tab):
	if tab == "graph":
		style = {"width": "98%", "height": "380px", "display": "block"}
	else:
		return {"display": "none"}


@app.callback(
	dash.dependencies.Output("graph_dropdown", "options"),
	[dash.dependencies.Input("score_button", "n_clicks")],
	prevent_initial_call=True)
def tabs_content_graphing2(clicks):
	global scoring_output
	jstr = json.loads(scoring_output)
	value = jstr[0]
	flat = json_flatten(value, "")
	l = list(flat.keys())
	return convert_list(l)

@app.callback(
	dash.dependencies.Output("graphing", "figure"),
	[dash.dependencies.Input("graph_dropdown", "value")],
	prevent_initial_call=True)
def tabs_content_graphing3(graph_dropdown_value):
	global scoring_output
	jstr = json.loads(scoring_output)
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

@app.callback(
	dash.dependencies.Output("scoring_datatable", "columns"),
	[dash.dependencies.Input("score_button", "n_clicks")],
	prevent_initial_call=True)
def tabs_content_scoring_tab3(clicks):
	global scoring_output
	jstr = json.loads(scoring_output)
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
	[dash.dependencies.Input("score_button", "n_clicks")],
	prevent_initial_call=True)
def tabs_content_scoring_tab2(clicks):
	global scoring_output
	jstr = json.loads(scoring_output)
	data_points = []
	for value in jstr:
		flat = json_flatten(value, "")
		data_points.append(flat)
	return data_points


@app.callback(
	dash.dependencies.Output("login_component", "style"),
	[
		dash.dependencies.Input("id_1", "n_clicks_timestamp"),
		dash.dependencies.Input("id_2", "n_clicks_timestamp")
	],
)
def toggle_collapse(input1, input2):
	btn_df = pd.DataFrame({"input1": [input1], "input2": [input2]})
	btn_df = btn_df.fillna(0)

	if btn_df.idxmax(axis=1).values == "input1":
		return {}
	if btn_df.idxmax(axis=1).values == "input2":
		return {"display": "none"}
	

@app.callback(
	dash.dependencies.Output("scoring_component", "style"),
	[
		dash.dependencies.Input("id_1", "n_clicks_timestamp"),
		dash.dependencies.Input("id_2", "n_clicks_timestamp")
	],
	prevent_initial_call=True)
def toggle_collapse(input1, input2):
	btn_df = pd.DataFrame({"input1": [input1], "input2": [input2]})
	btn_df = btn_df.fillna(0)

	if btn_df.idxmax(axis=1).values == "input1":
		return {"display": "none"}
	if btn_df.idxmax(axis=1).values == "input2":
		return {}
if __name__ == "__main__":
	app.run_server(debug=True)
