window.dash_clientside = Object.assign({}, window.dash_clientside, {
	clientside: {
		amcharter_serpentine: function(data_buffer, target_div, datetime_format) {
		 	am4core.ready(function() {
				// Themes begin
				am4core.useTheme(am4themes_animated);
				// Themes end
				am4core.disposeAllCharts();
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
				dateAxis.baseInterval = { count: 1, timeUnit: "day" };
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