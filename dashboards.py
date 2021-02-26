#http://127.0.0.1:8050/ 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import State
import plotly.graph_objects as go
from datetime import date
from dateutil.relativedelta import relativedelta
import data
import flask

dr = data.DataReader()
pos = dr.getPos()
nu = dr.getNu()
min_date = dr.getEarliestDate()
max_date = dr.getLatestDate()
max_date_p1 = dr.getLatestDateP1()
max_date_m1m = dr.getLatestDateM1M()

dropdown_nu = [{"label": "__all_transaction_types__", "value": "__all_transaction_types__"}] 
for entry in nu:
	dropdown_nu.append({"label": entry, "value": entry})

app = dash.Dash(__name__)
server = app.server


app.layout = html.Div([
		html.Label("Users:"),
		html.Div([ #Row
				html.Div([ #Column
						dcc.Dropdown(
							id="Dropdown",
							options=dropdown_nu,
							value=nu,
							multi=True,
							clearable=True,
							persistence=True
						),
					],
					style={"display": "inline-block", "verticalAlign": "top", "width": "85%"}
				),
				html.Div([
						html.Button("Add All",
									id="all_user_button", 
									type="text",
									style={
										"width": "100%",
										"height": "100%"
									}
						)
					],
					style={"display": "inline-block", "verticalAlign": "top", "width": "10%"}
				)
			]
		),
		html.Label("Algorithms:"),
		html.Div([ #Row
				dcc.Dropdown(
					id="algo_dropdown",
					options=[
						{"label": "Betweenness", "value": "Betweenness Centrality"},
						{"label": "Closeness", "value": "Closeness Centrality"}
					],
					value="Betweenness Centrality"
				)
			]
		),
		html.Div([ # Row
				html.Div([ # Column
						dcc.DatePickerRange(
							id="left_dpr",
							min_date_allowed=min_date,
							max_date_allowed=max_date_p1,
							start_date=max(max_date_m1m, min_date),
							end_date=max_date,
							display_format="Do MMM YYYY",
							number_of_months_shown=1,
							stay_open_on_select=True,
							with_portal=True,
							updatemode="singledate",
							day_size=80,
							style={"width": "100vx"},
						),
						dcc.Loading([
								dcc.Graph(
									id="transactions_left",
									figure={}
								)
							],
							id="transactions_left_loading",
							type="default",
							color="rgb(17,157,255)"
						)
					],
					style={"display": "inline-block", "verticalAlign": "top", "width": "50%"}
				),
				html.Div([
						dcc.DatePickerRange(
							id="right_dpr",
							min_date_allowed=min_date,
							max_date_allowed=max_date_p1,
							start_date=max(max_date_m1m, min_date),
							end_date=max_date,
							display_format="Do MMM YYYY",
							number_of_months_shown=1,
							stay_open_on_select=True,
							with_portal=True,
							updatemode="singledate",
							day_size=80,
							style={"width": "100vx"},
						),
						dcc.Loading([
								dcc.Graph(
									id="transactions_right",
									figure={}
								)
							],
							id="transactions_right_loading",
							type="default",
							color="rgb(17,157,255)"
						)
					],
					style={"display": "inline-block", "verticalAlign": "top", "width": "50%"}
				)
			],
			style={"width": "100%"}
		)
	]
)

def node_weighted_graph(dropdown_value, datepicker_start_date, datepicker_end_date, algorithm):
	df = data.DataFilter(pos)
	traces = []
	filtered = df.filter(dropdown_value, datepicker_start_date, datepicker_end_date)
	edge_counts = df.getEdgeCount()
	algolist = None
	if algorithm == "Betweenness Centrality":
		algolist = df.getBetweennessCentrality()
	if algorithm == "Closeness Centrality":
		algolist = df.getClosenessCentrality()

	algo_nu = [algolist[name] for name in filtered["nu_names"]]
	algo_nt = [algolist[name] for name in filtered["nt_names"]]

	traces.append(go.Scatter(x = filtered["Xed"],
							y = filtered["Yed"],
							name = "Edges",
							mode = "lines",
							line = dict(shape="spline", color="rgba(80,80,80,0.5)", width=1),
							text = ["{} -> {}<br>&nbsp;&nbsp;&nbsp;&nbsp;number of interactions: {}".format(m[0], m[1], n) for n, m in zip(edge_counts, filtered["edge_names"])],
							hoverinfo = "text"
				)
	)
	traces.append(
		go.Scatter(x = filtered["nu_xv"],
				y = filtered["nu_yv"],
				mode = "markers",
				name = "Users",
				marker = dict(symbol = "circle",
					size = 20,
					opacity=0.5,
					color = algo_nu,
					colorscale="greens",
					showscale=True,
					colorbar={
						"yanchor": "top",
						# "xanchor": "left",
						"x": 1,
						"y": 1,
						"ticks": "outside",
						"title": algorithm
					},
					# color = "rgb(89,205,105)",
					# color = "#6959CD",
					line = dict(color="darkgreen", width=2.0)
					),
				text = ["{}: {}".format(m, n) for m, n in zip(filtered["nu_names"], algo_nu)],
				hoverinfo = "text"
		)
	)
	traces.append(go.Scatter(x = filtered["nt_xv"],
							y = filtered["nt_yv"],
							mode = "markers",
							name = "Transaction Types",
							marker = dict(symbol = "circle",
								size = 15,
								opacity=0.5,
								color = algo_nt,
								colorscale="purples",
								showscale=True,
								colorbar={
									"yanchor": "top",
									# "xanchor": "left",
									"x": 1.2,
									"y": 1,
									"ticks": "outside",
									"title": "."
								},
								# color = "rgb(150,89,205)",
								# color = "#6959CD",
								line = dict(color="darkmagenta", width=1)
								),
							text = ["{}: {}".format(m, n) for m, n in zip(filtered["nt_names"], algo_nt)],
							# text = filtered["nt_names"],
							hoverinfo = "text"
				)
	)
	layout = go.Layout(
					hovermode="closest",
					xaxis={
						"showgrid": False, 
						"zeroline": False, 
						# "visible": False,
						"showticklabels": False,
						"linecolor": "black",
						"linewidth": 2,
						"mirror": True
					},
					yaxis={
						"showgrid": False, 
						"zeroline": False, 
						# "visible": False,
						"showticklabels": False,
						"linecolor": "black",
						"linewidth": 2,
						"mirror": True
					},
					legend_orientation="h"
	)
	figure = {"data": traces, "layout": layout}
	return figure

def graph_user_name_filter(dropdown_value, datepicker_start_date, datepicker_end_date, algorithm):
	if algorithm == "Betweenness Centrality":
		return node_weighted_graph(dropdown_value, datepicker_start_date, datepicker_end_date, algorithm)
	if algorithm == "Closeness Centrality":
		return node_weighted_graph(dropdown_value, datepicker_start_date, datepicker_end_date, algorithm)

# User Dropdown
@app.callback(
	dash.dependencies.Output("transactions_left", "figure"),
	[
		dash.dependencies.Input("Dropdown", "value"),
		dash.dependencies.Input("left_dpr", "start_date"),
		dash.dependencies.Input("left_dpr", "end_date"),
		dash.dependencies.Input("algo_dropdown", "value")
	]
)
def callback_left_datepicker(dropdown_value, datepicker_start_date, datepicker_end_date, algorithm):
	return graph_user_name_filter(dropdown_value, datepicker_start_date, datepicker_end_date, algorithm)

@app.callback(
	dash.dependencies.Output("transactions_right", "figure"),
	[
		dash.dependencies.Input("Dropdown", "value"),
		dash.dependencies.Input("right_dpr", "start_date"),
		dash.dependencies.Input("right_dpr", "end_date"),
		dash.dependencies.Input("algo_dropdown", "value")
	]
)
def callback_right_datepicker(dropdown_value, datepicker_start_date, datepicker_end_date, algorithm):
	return graph_user_name_filter(dropdown_value, datepicker_start_date, datepicker_end_date, algorithm)

# Buttons
@app.callback(
	dash.dependencies.Output("Dropdown", "value"),
	[dash.dependencies.Input("all_user_button", "n_clicks")],
	state=[State(component_id="Dropdown", component_property="value")], 
	prevent_initial_call=True)
def callback_all_button(n_clicks, dropdown_value):
	nu = dr.getAllNu()
	if "__all_transaction_types__" in dropdown_value:
		nu.insert(0, "__all_transaction_types__")
	return nu

# DatePickerRange
@app.callback(
	dash.dependencies.Output("left_dpr", "initial_visible_month"),
	[dash.dependencies.Input("left_dpr", "start_date"), dash.dependencies.Input("left_dpr", "end_date")],
	prevent_initial_call=True)
def callback_change_calendar_left(start_date, end_date):
	ctx = dash.callback_context
	if ctx.triggered:
		triggered = ctx.triggered[0]["prop_id"].split(".")[1]
		if triggered == "start_date":
			return start_date
		if triggered == "end_date":
			return end_date
	return start_date

if __name__ == "__main__":
	app.run_server(debug=True)