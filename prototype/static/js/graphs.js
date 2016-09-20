queue()
    .defer(d3.json, "static/data/br-states.json")
    .defer(d3.json, "/data/incidence-color-alerts/" + $('#interval').val())
    .defer(d3.json, "/data/weekly-incidence-curve")
    .await(makeGraphs);

function getColor(d) {
    return d == 4 ? '#ff0000' :
           d == 3 ? '#ff9900' :
           d == 2 ? '#f0ff00' :
                    '#30c130';
}

function makeGraphs(
    error, statesJson, incidenceColorAlerts, incidence
) {
    //Clean projectsJson data
    var dateFormat = d3.time.format("%Y-%m-%d");

    //Create a Crossfilter instance
    var ndx = crossfilter(incidence);

    //Define Dimensions
    var weekDim = ndx.dimension(function(d) { return d["isoweek"]; });
    var stateDim = ndx.dimension(function(d) { return d["uf"]; });
    var incidenceDim  = ndx.dimension(function(d) { return d["incidence"]; });


    //Calculate metrics
    var numIncidenceByWeek = weekDim.group(); 
    var totalIncidenceByState = stateDim.group().reduceSum(function(d) {
        return d["incidence"];
    });

    var all = ndx.groupAll();
    var totalIncidence = ndx.groupAll().reduceSum(function(d) {return d["incidence"];});

    var max_state = 4;

    //Define values (to be used in charts)
    var minWeek = weekDim.bottom(1)[0]["isoweek"];
    var maxWeek = weekDim.top(1)[0]["isoweek"];

    //Charts
    var weekChart = dc.barChart("#week-chart");
    var brChart = dc.geoChoroplethChart("#br-chart");
    var numberIncidenceND = dc.numberDisplay("#number-incidence-nd");
    var totalIncidenceND = dc.numberDisplay("#total-incidence-nd");

    numberIncidenceND
        .formatNumber(d3.format("d"))
        .valueAccessor(function(d){return d; })
        .group(all);

    totalIncidenceND
        .formatNumber(d3.format("d"))
        .valueAccessor(function(d){return d; })
        .group(totalIncidence)
        .formatNumber(d3.format(".3s"));

    weekChart
        .width(600)
        .height(160)
        .margins({top: 10, right: 50, bottom: 30, left: 50})
        .dimension(weekDim)
        .group(numIncidenceByWeek)
        .transitionDuration(500)
        .x(d3.time.scale().domain([minWeek, maxWeek]))
        .elasticY(true)
        .xAxisLabel("Week")
        .yAxis().ticks(4);

    brChart.width(1000)
        .height(330)
        .dimension(stateDim)
        .group(totalIncidenceByState)
        .colors(["#E2F2FF", "#C4E4FF", "#9ED2FF", "#81C5FF", "#6BBAFF", "#51AEFF", "#36A2FF", "#1E96FF", "#0089FF", "#0061B5"])
        .colorDomain([0, max_state])
        .overlayGeoJson(statesJson["features"], "state", function (d) {
            return d.properties.name;
        })
        .projection(d3.geo.equirectangular()
                    .scale(600)
                    .translate([-10, -30]))
        .title(function (p) {
            return "State: " + p["key"]
                    + "\n"
                    + "Total Incidence: " + Math.round(p["value"]) + " $";
        })

    dc.renderAll();
};
