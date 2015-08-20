$(document).ready(function() {
    $(test_chart).highcharts({
	chart: chart,
	title: title,
	plotOptions: plotOptions,
	xAxis: xAxis,
	yAxis: yAxis,
	series: series,
	tooltip: tooltip
    });
});
