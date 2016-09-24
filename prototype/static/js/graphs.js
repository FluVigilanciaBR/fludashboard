queue()
    .defer(d3.json, "static/data/br-states.json")
    .defer(d3.json, "/data/incidence-color-alerts/" + $('#interval').val())
    .defer(d3.json, "/data/weekly-incidence-curve/" + $('#interval').val())
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
    //Create a Crossfilter instance
    var ndx = crossfilter(incidence);

    //Define Dimensions
    var stateDim = ndx.dimension(function(d) { return d["UF"]; });
    var incidenceDim = ndx.dimension(function(d) { return d["incidence"]; });
    var alertDim = ndx.dimension(function(d) {return d['alert']});

    //Calculate metrics
    var totalIncidenceByState = stateDim.group().reduceSum(function(d) {
        return d["incidence"];
    });

    var all = ndx.groupAll();
    var totalIncidence = ndx.groupAll().reduceSum(function(d) {return d["incidence"];});


    //Charts
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

    brChart.width(1000)
        .height(330)
        .dimension(stateDim)
        .group(totalIncidenceByState)
        .colors(['#ff0000', '#ff9900', '#f0ff00', '#30c130'])
        .colorDomain([1, 4])
        .overlayGeoJson(statesJson["features"], "state", function (d) {
            return d.properties.nome;
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
