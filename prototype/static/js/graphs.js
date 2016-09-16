queue()
    .defer(d3.json, "static/data/br-states.json")
    .defer(d3.json, "/data/weekly-incidence-curve")
    .await(makeGraphs);

function makeGraphs(error, states_json, weekly_incidence_json) {
	
	//Clean projectsJson data
    var weekly_incidence = weekly_incidence_json;
    /*
	var dateFormat = d3.time.format("%Y-%m-%d");
	donorschooseProjects.forEach(function(d) {
		d["date_posted"] = dateFormat.parse(d["date_posted"].substring(0, 10));
		d["date_posted"].setDate(1);
		d["total_donations"] = +d["total_donations"];
	});
    */

	//Create a Crossfilter instance
	var ndx = crossfilter(weekly_incidence);

	//Define Dimensions
	//var totalDonationsDim  = ndx.dimension(function(d) { return d["total_donations"]; });
    var state_dim = ndx.dimension(function(d) {return d['uf'];});
    var week_dim = ndx.dimension(function(d) {return d['isoweek'];});

	//Calculate metrics
	//var numProjectsByResourceType = resourceTypeDim.group();
	/*var totalDonationsByState = stateDim.group().reduceSum(function(d) {
		return d["total_donations"];
	});*/
    var max_state = 1000;

	var all = ndx.groupAll();

	//Define values (to be used in charts)
	var min_week = week_dim.bottom(1)[0]["isoweek"];
	var max_week = week_dim.top(1)[0]["isoweek"];

    //Charts
	//var timeChart = dc.barChart("#time-chart");
	//var resourceTypeChart = dc.rowChart("#resource-type-row-chart");
	//var usChart = dc.geoChoroplethChart("#us-chart");
	//var totalDonationsND = dc.numberDisplay("#total-donations-nd");
    var br_chart = dc.geoChoroplethChart('#br-chart');

    /*
	numberProjectsND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(all);

	totalDonationsND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(totalDonations)
		.formatNumber(d3.format(".3s"));

	timeChart
		.width(600)
		.height(160)
		.margins({top: 10, right: 50, bottom: 30, left: 50})
		.dimension(dateDim)
		.group(numProjectsByDate)
		.transitionDuration(500)
		.x(d3.time.scale().domain([minDate, maxDate]))
		.elasticY(true)
		.xAxisLabel("Year")
		.yAxis().ticks(4);

	resourceTypeChart
        .width(300)
        .height(250)
        .dimension(resourceTypeDim)
        .group(numProjectsByResourceType)
        .xAxis().ticks(4);

	povertyLevelChart
		.width(300)
		.height(250)
        .dimension(povertyLevelDim)
        .group(numProjectsByPovertyLevel)
        .xAxis().ticks(4);


	usChart.width(1000)
		.height(330)
		.dimension(stateDim)
		.group(totalDonationsByState)
		.colors(["#E2F2FF", "#C4E4FF", "#9ED2FF", "#81C5FF", "#6BBAFF", "#51AEFF", "#36A2FF", "#1E96FF", "#0089FF", "#0061B5"])
		.colorDomain([0, max_state])
		.overlayGeoJson(statesJson["features"], "state", function (d) {
			return d.properties.name;
		})
		.projection(d3.geo.albersUsa()
    				.scale(600)
    				.translate([340, 150]))
		.title(function (p) {
			return "State: " + p["key"]
					+ "\n"
					+ "Total Donations: " + Math.round(p["value"]) + " $";
		})
    */

    br_chart.width(1000)
		.height(330)
		.dimension(state_dim)
		.group(100000)
		.colors(["#E2F2FF", "#C4E4FF", "#9ED2FF", "#81C5FF", "#6BBAFF", "#51AEFF", "#36A2FF", "#1E96FF", "#0089FF", "#0061B5"])
		.colorDomain([0, max_state])
		.overlayGeoJson(states_json["features"], "state", function (d) {
			return d.properties.name;
		})
		.projection(d3.geo.albersUsa()
    				.scale(600)
    				.translate([340, 150]))
		.title(function (p) {
            return 'State:';
			return "State: " + p["key"]
					+ "\n"
					+ "Total Donations: " + Math.round(p["value"]) + " $";
		})

    dc.renderAll();

};
