#http://127.0.0.1:8050/ 
import dash
import dash_core_components as dcc
import dash_html_components as html
import flask


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
		html.Button("hello", id="but"),
		html.Div(id="container", style={"width": "800px", "height": "600px", "border": "1px solid grey"}),
		html.Script("", src="C://Users/Ramsay/node_modules/monaco-editor/min/vs/loader.js"),
		html.Script("""
			require.config({ paths: { vs: 'C://Users/Ramsay/node_modules/monaco-editor/min/vs' } });

			require(['vs/editor/editor.main'], function () {
				var editor = monaco.editor.create(document.getElementById('container'), {
					value: ['function x() {', '\tconsole.log("Hello world!");', '}'].join('\n'),
					language: 'javascript'
				});
			});
		"""),
	]
)

app.clientside_callback(
	dash.dependencies.ClientsideFunction(
		namespace="clientside",
		function_name="monaco_setup"
	),
	dash.dependencies.Output("container", "style"),
	[dash.dependencies.Input("but", "n_clicks")],
	prevent_initial_call=True)

if __name__ == "__main__":
	app.run_server(debug=True)
