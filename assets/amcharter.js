window.dash_clientside = Object.assign({}, window.dash_clientside, {
	clientside: {
		amcharter_daily: function(data_buffer, datetime, target_div, datetime_format) {
			var parsed_datetime = new Date(datetime);
			var parsed_year = parsed_datetime.getFullYear();
			var parsed_month = parsed_datetime.getMonth();
			var parsed_day = parsed_datetime.getDate();
			am4core.ready(function() {

			// Themes begin
			am4core.useTheme(am4themes_animated);
			// Themes end
			// am4core.disposeAllCharts();
			document.getElementById(target_div).innerHTML = "";
					
			var icons = {
				"work":"data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pg0KPCEtLSBHZW5lcmF0b3I6IEFkb2JlIElsbHVzdHJhdG9yIDE2LjAuMCwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDYuMDAgQnVpbGQgMCkgIC0tPg0KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4NCjxzdmcgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB4PSIwcHgiIHk9IjBweCINCgkgd2lkdGg9Ijc3OS4xMXB4IiBoZWlnaHQ9Ijc3OS4xMXB4IiB2aWV3Qm94PSIwIDAgNzc5LjExIDc3OS4xMSIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgNzc5LjExIDc3OS4xMTsiDQoJIHhtbDpzcGFjZT0icHJlc2VydmUiPg0KPGc+DQoJPGc+DQoJCTxwYXRoIGQ9Ik02NjIuOTE0LDYzMi4zNTFINTMwLjA3SDI1NC40NzRjLTExLjQ5LDAtMjAuODA2LDkuMzE1LTIwLjgwNiwyMC44MDZ2MTIuODA1YzAsMTEuNDksOS4zMTUsMjAuODEsMjAuODA2LDIwLjgxaDI3NS41OTgNCgkJCWgxMzIuODQ0aDY4Ljgydi01NC40MThMNjYyLjkxNCw2MzIuMzUxTDY2Mi45MTQsNjMyLjM1MXoiLz4NCgkJPGNpcmNsZSBjeD0iMjExLjE4NyIgY3k9IjE4OS42MjUiIHI9IjExNS4xOSIvPg0KCQk8cGF0aCBkPSJNNDkyLjIzNCw0NzIuMTQ3bC0yNjMuOTY5LTAuMTQ2bC02LjI1LTAuMDJ2LTMwLjYzMmwtMC4yMTctMjUuNjRjMC02MS4yNDUtNDkuNjUxLTExMC44OTgtMTEwLjg5OS0xMTAuODk4DQoJCQljLTIuMDc1LDAtNC4xMzYsMC4wNy02LjE4NCwwLjE4MmwtMC4xNTYtMC4xODJDNDYuODEzLDMwNC44MTMsMCwzNTEuNjI1LDAsNDA5LjM3MnYyOTUuMzAzaDIyMi4wMTVWNTc4Ljg3NmwtMi45MzctMC4yMzENCgkJCWMtMC4yMDktMC4wMTktMC4yNjEsMC4wMDItMC4zOTEsMC4wMDJjLTE1LjAyMSwwLTI5LjQxNy02LjMyNC0zOS41NjItMTcuMzk5bC05MC4xMTItOTguMzYzDQoJCQljLTIuODczLTMuMTM1LTIuNjYtOC4wMDMsMC40NzYtMTAuODc0YzMuMTMzLTIuODczLDguMDAzLTIuNjU5LDEwLjg3NCwwLjQ3Nmw5MC4xMTEsOTguMzYyDQoJCQljNy4zMjIsNy45OTMsMTcuNjQ4LDEyLjg4MSwyOC41MjEsMTMuMDM5YzAuNzIzLDAuMDEsMTAuNTk0LDAuMTUyLDEwLjU5NCwwLjE1MmgyNjIuNjQ1YzI1LjM3NSwwLDQ1Ljk0Ny0yMC41NzEsNDUuOTQ3LTQ1Ljk0Nw0KCQkJQzUzOC4xODIsNDkyLjcxNyw1MTcuNjA5LDQ3Mi4xNDcsNDkyLjIzNCw0NzIuMTQ3eiIvPg0KCQk8cGF0aCBkPSJNNzY1LjE5NywzMDkuMTExYy0xMC43NDQtMy42ODEtMjIuNDM5LDIuMDQ5LTI2LjEyMywxMi43OTRsLTg3LjIwOSwyNTQuNTlIMzM5LjgwM2MtMTEuMzU2LDAtMjAuNTY3LDkuMjA2LTIwLjU2NywyMC41NjQNCgkJCXM5LjIxMSwyMC41NjYsMjAuNTY3LDIwLjU2NmgzMjYuNTA3YzYuOTk0LDAsMTMuMTY4LTMuNTAzLDE2Ljg3OS04Ljg0MWMxLjI4My0xLjY5NCwyLjMzLTMuNjA3LDMuMDU5LTUuNzI5TDc3OCwzMzUuMjI1DQoJCQlDNzgxLjY3LDMyNC40ODYsNzc1Ljk0NywzMTIuNzksNzY1LjE5NywzMDkuMTExeiIvPg0KCTwvZz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjwvc3ZnPg0K",
				"dance":"data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pg0KPCEtLSBHZW5lcmF0b3I6IEFkb2JlIElsbHVzdHJhdG9yIDE2LjAuMCwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDYuMDAgQnVpbGQgMCkgIC0tPg0KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4NCjxzdmcgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB4PSIwcHgiIHk9IjBweCINCgkgd2lkdGg9IjI0OC45MTRweCIgaGVpZ2h0PSIyNDguOTE0cHgiIHZpZXdCb3g9IjAgMCAyNDguOTE0IDI0OC45MTQiIHN0eWxlPSJlbmFibGUtYmFja2dyb3VuZDpuZXcgMCAwIDI0OC45MTQgMjQ4LjkxNDsiDQoJIHhtbDpzcGFjZT0icHJlc2VydmUiPg0KPGc+DQoJPGc+DQoJCTxwYXRoIGQ9Ik0yMDEuNzExLDQ5LjU4M2MtNS40NiwwLTkuODk1LDMuNzcxLTkuODk1LDguNDE5YzAsNC42NTMsNC40MzUsOC40MTksOS44OTUsOC40MTljNS4zMTYsMCw5LjY0My0zLjU2Niw5Ljg3Ni04LjAzMg0KCQkJYzUuMTA1LTEzLjYsNC4xMDYtMjQuMDc4LDMuMDQzLTI5LjEzN2MtMC43NDctMy41MzMtNC4yLTYuMjk1LTcuODUxLTYuMjk1bC0yMy4yNy0wLjAxYy0xLjg1NywwLTMuNTk0LDAuNzI0LTQuOSwyLjAzDQoJCQljLTEuMzgyLDEuMzkxLTIuMTM4LDMuMjc2LTIuMTI5LDUuMzJjMC4wMzgsNS42OTktMS4yMjMsMTMuMzA2LTIuMzA1LDE4Ljc3NmMtMC45MDYtMC4yMzMtMS44NzctMC4zNjQtMi44ODUtMC4zNjQNCgkJCWMtNS40NjEsMC05Ljg5NSwzLjc3MS05Ljg5NSw4LjQyNGMwLDQuNjQ4LDQuNDM4LDguNDE5LDkuODk1LDguNDE5YzUuMDU1LDAsOS4yMTMtMy4yMiw5LjgxOS03LjM3OGwwLjA3NSwwLjAxOQ0KCQkJYzAuMTYzLTAuNjUzLDMuODI2LTE1LjUyMyw0LjA3OS0yNi40NTNsMjAuODk4LDAuMDA5YzAuNjY4LDMuNjE3LDEuMTExLDkuOTgzLTEuMTI0LDE4LjMyMw0KCQkJQzIwMy45ODgsNDkuNzY1LDIwMi44NzgsNDkuNTgzLDIwMS43MTEsNDkuNTgzeiIvPg0KCQk8cGF0aCBkPSJNMzUuODY0LDEzNy44MzJjMi4wMjEsNC4xOTEsNy42NDksNS42NjEsMTIuNTY4LDMuMjk1YzQuNzkzLTIuMzAxLDcuMTQxLTcuMzkzLDUuNDE0LTExLjUxOQ0KCQkJYy0xLjMtMTQuNDcyLTYuNzQ0LTIzLjQ3NS05Ljg5Ni0yNy41NzdjLTIuMjA4LTIuODUyLTYuNTE1LTMuODUxLTkuODA4LTIuMjY0bC0yMC45NjksMTAuMDg1DQoJCQljLTEuNjczLDAuODAzLTIuOTI2LDIuMjA4LTMuNTMzLDMuOTU4Yy0wLjY0NCwxLjg0OS0wLjUwMSwzLjg4MywwLjM5Miw1LjcxN2MyLjUwNCw1LjEyLDQuNjY5LDEyLjUyMiw2LjA2LDE3LjkyMQ0KCQkJYy0wLjkyMSwwLjE4My0xLjg1MSwwLjQ4NS0yLjc1MywwLjkyNWMtNC45MTcsMi4zNjYtNy4yNzMsNy42ODctNS4yNTUsMTEuODc3YzIuMDIxLDQuMTkxLDcuNjQ1LDUuNjY2LDEyLjU2OSwzLjI5NQ0KCQkJYzQuNTQ4LTIuMTg4LDYuOS02LjkwMiw1LjY0Mi0xMC45MDZsMC4wNzctMC4wMTVjLTAuMTMzLTAuNjYyLTMuMjg4LTE1LjY0NC03Ljc5OS0yNS42MDhsMTguODMtOS4wNTQNCgkJCWMyLjE3LDIuOTczLDUuMzM0LDguNTEzLDYuOTM1LDE2Ljk5OGMtMS4wNzYsMC4xNjgtMi4xNTYsMC40OS0zLjIwOCwwLjk5NEMzNi4yMDIsMTI4LjMyLDMzLjg0NiwxMzMuNjQyLDM1Ljg2NCwxMzcuODMyeiIvPg0KCQk8Y2lyY2xlIGN4PSIxMTAuNTY1IiBjeT0iMzguMTM2IiByPSIyMS4wMDQiLz4NCgkJPHBhdGggZD0iTTE0LjMzNywyMzIuODY4aDIyMC4yMzljNy45MjEsMCwxNC4zMzgtNi4yNzIsMTQuMzM4LTE0LjAyMWMwLTcuNzQ3LTYuNDE3LTE0LjAyNC0xNC4zMzgtMTQuMDI0aC02Ny4yNjINCgkJCWMwLjM5My0wLjE0NSwwLjc5NC0wLjI4LDEuMTc2LTAuNTA0YzMuMjkxLTEuOTkzLDQuMzUxLTYuMjc3LDIuMzU3LTkuNTcybC0zOS4yNzgtNjUuMDE3di0zMi4xMQ0KCQkJYzE3Ljg4LDE2LjEzOSwyNi41MjMsNDEuOTg1LDI2LjY3Nyw0Mi40NTdjMC45NTcsMi45NDksMy42OTIsNC44MjUsNi42MzcsNC44MjVjMC43MDUsMCwxLjQzNC0wLjEwNiwyLjEzOC0wLjMzNg0KCQkJYzMuNjczLTEuMTgxLDUuNjgtNS4xMTUsNC40OTQtOC43NzNjLTAuNTg4LTEuODA3LTEyLjY2MS0zOC4yNjEtMzkuOTY5LTU1LjY5N2MtMC4xMTEtOS41MjUtNy44NTItMTcuMjE3LTE3LjQwNi0xNy4yMTdoLTcuMTU5DQoJCQljLTQuNTg3LDAtOC43MzIsMS44MTEtMTEuODQzLDQuNzA5Yy0yMS40NjQtMTUuMzIyLTMxLjc5LTQ2LjE5NC0zMS45NjItNDYuNzE3Yy0xLjE5LTMuNjU0LTUuMTA4LTUuNjctOC43NzQtNC40ODUNCgkJCWMtMy42NzEsMS4xODUtNS42NzgsNS4xMTUtNC40OTIsOC43NzRjMC41ODEsMS44MDEsMTIuNTY0LDM3Ljk4LDM5LjY0Miw1NS41MDF2NTUuNzkxTDc2LjA0NSwxNjAuMTUNCgkJCWMtMS4xMDQsMS45MzctMS4yMTgsNC4yNzktMC4yOTYsNi4zMTlsMTUuNjgxLDM0Ljc1MWMwLjc5MywxLjc2LDIuMjQ1LDIuOTc4LDMuOTE4LDMuNjAzSDE0LjMzNw0KCQkJQzYuNDE5LDIwNC44MjMsMCwyMTEuMTA1LDAsMjE4Ljg0OEMwLDIyNi41OTEsNi40MTksMjMyLjg2OCwxNC4zMzcsMjMyLjg2OHogTTg5LjkxNCwxNjMuOTY4bDEzLjMwMS0yMy4zMzVoMTguNjQ3bDM3LjA0Nyw2MS4zMjUNCgkJCWMwLjg0NSwxLjM5NiwyLjExNCwyLjMzOCwzLjUyOCwyLjg3aC02Mi4xNTZjMC4xMTktMC4wNDcsMC4yNDgtMC4wNjUsMC4zNjctMC4xMTdjMy41MDctMS41ODIsNS4wNzUtNS43MTIsMy40ODktOS4yMjINCgkJCUw4OS45MTQsMTYzLjk2OHoiLz4NCgk8L2c+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8L3N2Zz4NCg==",
			};

			am4core.ready(function() {
				var chart = am4core.create(target_div, am4plugins_timeline.CurveChart);
				chart.curveContainer.padding(100, 20, 50, 20);
				chart.maskBullets = false;

				var colorSet = new am4core.ColorSet();

				chart.dateFormatter.inputDateFormat = datetime_format;
				// chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm";
				chart.dateFormatter.inputDateFormat = datetime_format;
				// chart.dateFormatter.dateFormat = "HH";

				new_data = JSON.parse(data_buffer);
				new_data.sort(function(first, second) {
 					return new Date(first["start"]) - new Date(second["start"]);
				});
				for (i = 0; i < new_data.length; i++) {
					if ("icon" in new_data[i]) {
						new_data[i]["icon"] = icons[new_data[i]["icon"]];
					}
					if ("color_index" in new_data[i]) {
						new_data[i]["color"] = colorSet.getIndex(new_data[i]["color_index"]);
					}
				}
				chart.data = new_data;

				chart.fontSize = 10;
				chart.tooltipContainer.fontSize = 10;

				var categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
				categoryAxis.dataFields.category = "category";
				categoryAxis.renderer.grid.template.disabled = true;
				categoryAxis.renderer.labels.template.paddingRight = 25;
				categoryAxis.renderer.minGridDistance = 10;
				categoryAxis.renderer.innerRadius = 10;
				categoryAxis.renderer.radius = 30;

				var dateAxis = chart.xAxes.push(new am4charts.DateAxis());


				dateAxis.renderer.points = getPoints();


				dateAxis.renderer.autoScale = false;
				dateAxis.renderer.autoCenter = false;
				dateAxis.renderer.minGridDistance = 70;
				dateAxis.baseInterval = { count: 5, timeUnit: "seconds" };
				dateAxis.renderer.tooltipLocation = 0;
				dateAxis.renderer.line.strokeDasharray = "1,4";
				dateAxis.renderer.line.strokeOpacity = 0.5;
				dateAxis.tooltip.background.fillOpacity = 0.2;
				dateAxis.tooltip.background.cornerRadius = 5;
				dateAxis.tooltip.label.fill = new am4core.InterfaceColorSet().getFor("alternativeBackground");
				dateAxis.tooltip.label.paddingTop = 7;
				dateAxis.endLocation = 0;
				dateAxis.startLocation = -0.5;
				dateAxis.min = new Date(parsed_year, parsed_month, parsed_day, 0, 0).getTime();
				dateAxis.max = new Date(parsed_year, parsed_month, parsed_day, 23, 59).getTime();    

				var labelTemplate = dateAxis.renderer.labels.template;
				labelTemplate.verticalCenter = "middle";
				labelTemplate.fillOpacity = 0.6;
				labelTemplate.background.fill = new am4core.InterfaceColorSet().getFor("background");
				labelTemplate.background.fillOpacity = 1;
				labelTemplate.fill = new am4core.InterfaceColorSet().getFor("text");
				labelTemplate.padding(7, 7, 7, 7);

				var series = chart.series.push(new am4plugins_timeline.CurveColumnSeries());
				series.columns.template.height = am4core.percent(30);

				series.dataFields.openDateX = "start";
				series.dataFields.dateX = "end";
				series.dataFields.categoryY = "category";
				series.baseAxis = categoryAxis;
				series.columns.template.propertyFields.fill = "color"; // get color from data
				series.columns.template.propertyFields.stroke = "color";
				series.columns.template.strokeOpacity = 0;
				series.columns.template.fillOpacity = 0.6;

				var imageBullet1 = series.bullets.push(new am4plugins_bullets.PinBullet());
				imageBullet1.background.radius = 18;
				imageBullet1.locationX = 1;
				imageBullet1.propertyFields.stroke = "color";
				imageBullet1.background.propertyFields.fill = "color";
				imageBullet1.image = new am4core.Image();
				imageBullet1.image.propertyFields.href = "icon";
				imageBullet1.image.scale = 0.7;
				imageBullet1.circle.radius = am4core.percent(100);
				imageBullet1.background.fillOpacity = 0.8;
				imageBullet1.background.strokeOpacity = 0;
				imageBullet1.dy = -2;
				imageBullet1.background.pointerBaseWidth = 10;
				imageBullet1.background.pointerLength = 10
				imageBullet1.tooltipText = "{text}";

				series.tooltip.pointerOrientation = "up";

				imageBullet1.background.adapter.add("pointerAngle", (value, target) => {
					if (target.dataItem) {
						var position = dateAxis.valueToPosition(target.dataItem.openDateX.getTime());
						return dateAxis.renderer.positionToAngle(position);
					}
					return value;
				});

				var hs = imageBullet1.states.create("hover")
				hs.properties.scale = 1.3;
				hs.properties.opacity = 1;

				var textBullet = series.bullets.push(new am4charts.LabelBullet());
				textBullet.label.propertyFields.text = "text";
				textBullet.disabled = true;
				textBullet.propertyFields.disabled = "textDisabled";
				textBullet.label.strokeOpacity = 0;
				textBullet.locationX = 1;
				textBullet.dy = - 100;
				textBullet.label.textAlign = "middle";

				chart.scrollbarX = new am4core.Scrollbar();
				chart.scrollbarX.align = "center"
				chart.scrollbarX.width = am4core.percent(75);
				chart.scrollbarX.parent = chart.curveContainer;
				chart.scrollbarX.height = 300;
				chart.scrollbarX.orientation = "vertical";
				chart.scrollbarX.x = 128;
				chart.scrollbarX.y = -140;
				chart.scrollbarX.isMeasured = false;
				chart.scrollbarX.opacity = 0.5;

				var cursor = new am4plugins_timeline.CurveCursor();
				chart.cursor = cursor;
				cursor.xAxis = dateAxis;
				cursor.yAxis = categoryAxis;
				cursor.lineY.disabled = true;
				cursor.lineX.disabled = true;

				dateAxis.renderer.tooltipLocation2 = 0;
				categoryAxis.cursorTooltipEnabled = false;

				chart.zoomOutButton.disabled = true;

				var previousBullet;

				// chart.events.on("inited", function() {
				// 	setTimeout(function() {
				// 		hoverItem(series.dataItems.getIndex(0));
				// 	}, 2000)
				// })

				// function hoverItem(dataItem) {
				// 	var bullet = dataItem.bullets.getKey(imageBullet1.uid);
				// 	var index = dataItem.index;

				// 	if (index >= series.dataItems.length - 1) {
				// 		index = -1;
				// 	}

				// 	if (bullet) {

				// 		if (previousBullet) {
				// 			previousBullet.isHover = false;
				// 		}

				// 		bullet.isHover = true;

				// 		previousBullet = bullet;
				// 	}
				// 	setTimeout(
				// 		function() {
				// 			hoverItem(series.dataItems.getIndex(index + 1))
				// 		}, 1000);
				// }

			});


			function getPoints() {

			    var points = [{ x: -650, y: 200 }, { x: 0, y: 200 }];
			    // var points = [{ x: -1300, y: 200 }, { x: 0, y: 200 }];

			    var w = 400;
			    var h = 400;
			    var levelCount = 4;

			    var radius = am4core.math.min(w / (levelCount - 1) / 2, h / 2);
			    var startX = radius;

			    for (var i = 0; i < 25; i++) {
			        var angle = 0 + i / 25 * 90;
			        var centerPoint = { y: 200 - radius, x: 0 }
			        points.push({ y: centerPoint.y + radius * am4core.math.cos(angle), x: centerPoint.x + radius * am4core.math.sin(angle) });
			    }


			    for (var i = 0; i < levelCount; i++) {

			        if (i % 2 != 0) {
			            points.push({ y: -h / 2 + radius, x: startX + w / (levelCount - 1) * i })
			            points.push({ y: h / 2 - radius, x: startX + w / (levelCount - 1) * i })

			            var centerPoint = { y: h / 2 - radius, x: startX + w / (levelCount - 1) * (i + 0.5) }
			            if (i < levelCount - 1) {
			                for (var k = 0; k < 50; k++) {
			                    var angle = -90 + k / 50 * 180;
			                    points.push({ y: centerPoint.y + radius * am4core.math.cos(angle), x: centerPoint.x + radius * am4core.math.sin(angle) });
			                }
			            }

			            if (i == levelCount - 1) {
			                points.pop();
			                points.push({ y: -radius, x: startX + w / (levelCount - 1) * i })
			                var centerPoint = { y: -radius, x: startX + w / (levelCount - 1) * (i + 0.5) }
			                for (var k = 0; k < 25; k++) {
			                    var angle = -90 + k / 25 * 90;
			                    points.push({ y: centerPoint.y + radius * am4core.math.cos(angle), x: centerPoint.x + radius * am4core.math.sin(angle) });
			                }
			                points.push({ y: 0, x: 650 });
			                // points.push({ y: 0, x: 1300 });
			            }

			        }
			        else {
			            points.push({ y: h / 2 - radius, x: startX + w / (levelCount - 1) * i })
			            points.push({ y: -h / 2 + radius, x: startX + w / (levelCount - 1) * i })
			            var centerPoint = { y: -h / 2 + radius, x: startX + w / (levelCount - 1) * (i + 0.5) }
			            if (i < levelCount - 1) {
			                for (var k = 0; k < 50; k++) {
			                    var angle = -90 - k / 50 * 180;
			                    points.push({ y: centerPoint.y + radius * am4core.math.cos(angle), x: centerPoint.x + radius * am4core.math.sin(angle) });
			                }
			            }
			        }
			    }

			    return points;
			}

			}); // end am4core.ready()
			return "";
        },

        amcharter_serpentine: function(data_buffer, target_div, datetime_format) {
		 	am4core.ready(function() {
				// Themes begin
				am4core.useTheme(am4themes_animated);
				// Themes end
				// am4core.disposeAllCharts();
				document.getElementById(target_div).innerHTML = "";
				var chart = am4core.create(target_div, am4plugins_timeline.SerpentineChart);
				chart.curveContainer.padding(50, 20, 50, 20);
				chart.levelCount = 4;
				chart.yAxisRadius = am4core.percent(25);
				chart.yAxisInnerRadius = am4core.percent(-25);
				chart.maskBullets = false;

				var colorSet = new am4core.ColorSet();
				colorSet.saturation = 0.5;

				var color_range = 15;
				var cat_list = [];
				new_data = JSON.parse(data_buffer);
				for (i = 0; i < new_data.length; i++) {
					if ("category"  in new_data[i]) {
						cat_list.push(new_data[i]["category"]);
					}
				}
				var uniq_list = [...new Set(cat_list)];
				var uniq_len = uniq_list.length;
				var iter = color_range / uniq_len;
				for (i = 0; i < new_data.length; i++) {
					if ("category"  in new_data[i]) {
						var index = uniq_list.indexOf(new_data[i]["category"]);
						var colorindex = Math.floor(index*iter);
						new_data[i]["color"] = colorSet.getIndex(colorindex);
						
					}
				}
				chart.data = new_data;


				chart.dateFormatter.dateFormat = datetime_format;
				chart.dateFormatter.inputDateFormat = datetime_format;
				chart.fontSize = 11;

				var categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
				categoryAxis.dataFields.category = "category";
				categoryAxis.renderer.grid.template.disabled = true;
				categoryAxis.renderer.labels.template.paddingRight = 25;
				categoryAxis.renderer.minGridDistance = 10;
				categoryAxis.renderer.innerRadius = -60;
				categoryAxis.renderer.radius = 60;

				var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
				dateAxis.renderer.minGridDistance = 70;
				// dateAxis.baseInterval = { count: 1, timeUnit: "day" };
				dateAxis.baseInterval = { count: 5, timeUnit: "seconds" };
				dateAxis.renderer.tooltipLocation = 0;
				dateAxis.startLocation = -0.5;
				dateAxis.renderer.line.strokeDasharray = "1,4";
				dateAxis.renderer.line.strokeOpacity = 0.6;
				dateAxis.tooltip.background.fillOpacity = 0.2;
				dateAxis.tooltip.background.cornerRadius = 5;
				dateAxis.tooltip.label.fill = new am4core.InterfaceColorSet().getFor("alternativeBackground");
				dateAxis.tooltip.label.paddingTop = 7;

				var labelTemplate = dateAxis.renderer.labels.template;
				labelTemplate.verticalCenter = "middle";
				labelTemplate.fillOpacity = 0.7;
				labelTemplate.background.fill = new am4core.InterfaceColorSet().getFor("background");
				labelTemplate.background.fillOpacity = 1;
				labelTemplate.padding(7, 7, 7, 7);

				var series = chart.series.push(new am4plugins_timeline.CurveColumnSeries());
				series.columns.template.height = am4core.percent(20);
				series.columns.template.tooltipText = "{task}: [bold]{openDateX}[/] - [bold]{dateX}[/]";

				series.dataFields.openDateX = "start";
				series.dataFields.dateX = "end";
				series.dataFields.categoryY = "category";
				series.columns.template.propertyFields.fill = "color"; // get color from data
				series.columns.template.propertyFields.stroke = "color";
				series.columns.template.strokeOpacity = 0;

				var bullet = series.bullets.push(new am4charts.CircleBullet());
				bullet.circle.radius = 3;
				bullet.circle.strokeOpacity = 0;
				bullet.propertyFields.fill = "color";
				bullet.locationX = 0;


				var bullet2 = series.bullets.push(new am4charts.CircleBullet());
				bullet2.circle.radius = 3;
				bullet2.circle.strokeOpacity = 0;
				bullet2.propertyFields.fill = "color";
				bullet2.locationX = 1;

				chart.scrollbarX = new am4core.Scrollbar();
				chart.scrollbarX.align = "center"
				chart.scrollbarX.width = am4core.percent(85);

				var eventSeries = chart.series.push(new am4plugins_timeline.CurveLineSeries());
				eventSeries.dataFields.dateX = "start";
				eventSeries.dataFields.categoryY = "category";
				eventSeries.data = new_data
				// [
				// 	{ category: "Module #4", eventDate: "2019-01-15", letter: "As always", description: "Something happened here", color: colorSet.getIndex(15)},
				// 	{ category: "Module #1", eventDate: "2019-01-23", letter: "B", description: "Something happened here" },
				// 	{ category: "", eventDate: "2019-02-10", letter: "C", description: "Something happened here" },
				// 	{ category: "", eventDate: "2019-02-29", letter: "D", description: "Something happened here" },
				// 	{ category: "", eventDate: "2019-03-06", letter: "E", description: "Something happened here" },
				// 	{ category: "", eventDate: "2019-03-12", letter: "F", description: "Something happened here" },
				// 	{ category: "", eventDate: "2019-03-22", letter: "G", description: "Something happened here" }];
				// new_data[i]["color"] = colorSet.getIndex(colorindex);

				eventSeries.strokeOpacity = 0;

				var flagBullet = eventSeries.bullets.push(new am4plugins_bullets.FlagBullet())
				flagBullet.label.propertyFields.text = "task";
				flagBullet.locationX = 0;
				flagBullet.propertyFields.fill = "color";
				flagBullet.propertyFields.stroke = "color";
				flagBullet.tooltipText = "{task}: [bold]{start}[/] - [bold]{end}[/]";

				var cursor = new am4plugins_timeline.CurveCursor();
				chart.cursor = cursor;
				cursor.xAxis = dateAxis;
				cursor.yAxis = categoryAxis;
				cursor.lineY.disabled = true;
				cursor.lineX.strokeDasharray = "1,4";
				cursor.lineX.strokeOpacity = 1;

				dateAxis.renderer.tooltipLocation2 = 0;
				categoryAxis.cursorTooltipEnabled = false;
			});
			return "";
		}
    }
});