/** Dashboard class */
class Dashboard {
    constructor(
        userInterface, map
    ) {
        this.ui = userInterface;

        this.group_by = 'week'; // year or week
        this.separated_by = 'state'; // state or region
        this.flu_colors = {
            1: 'green',
            2: 'yellow',
            3: 'orange',
            4: 'red',
        };

        // create the tile layer with correct attribution
        this.map = L.map('map');
        this.osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
        this.osmAttrib='Map data © <a href="http://openstreetmap.org">' +
            'OpenStreetMap</a> contributors';
        this.osm = new L.TileLayer(
            this.osmUrl, {minZoom: 1, maxZoom: 12, attribution: this.osmAttrib}
        );

        // cheat
        this.divTableContent = '' +
        '<table id="data-table" ' +
        '  class="display table table-striped table-condensed">' +
        '  <!-- create a custom header -->' +
        '  <thead class="header">' +
        '    <tr class="header">' +
        '      <th>Unidade da Federa&ccedil;&atilde;o</th>' +
        '      <th>Semana</th>' +
        '      <th>Incidência (por 100 mil habitantes)</th>' +
        '    </tr>' +
        '  </thead>' +
        '</table>';

        this.divTable.html(this.divTableContent);
        this.data_table = this.divTable.DataTable();
        this.yearInput.change(this.load_graphs);
    }

    /**
     * start up the charts
     *
     */
    init() {
        this.map.setView([-16, -50.528742], 3);
        this.osm.addTo(this.map);
        this.load_graphs();
        this.weekDisplay.text(this.ui.week);
    }

    get geoJsonURL() {
        if (this.typeGeoStateInput.attr('checked')) {
            return 'static/data/br-states.json';
        } else {
            return 'static/data/br-regions.json';
        }
    }

    /**
     * load data and build charts
     *
     */
    load_graphs() {
        queue()
            .defer(d3.json, this.geoJsonUrl)
            .defer(d3.json, '/data/incidence/' + year)
            .await(makeGraphs);
    }


    /**
     * Plot incidence chart using
     * @param {number} year - year to filter the data
     * @param {string} state_name - state_name to filter the data
     * @param {number} week- week to filter the data
     */
    plot_incidence_chart(year, state_name, week) {
        if (state_name == '') {
            $('.chart-incidence').addClass('hidden');
            $('#vi .weekly-incidence-curve-chart').empty();
            return;
        } else {
            $('.chart-incidence').removeClass('hidden');
        }

        SRAGChart.plot(
            '#weekly-incidence-curve-chart',
            year, state_name, week
        );
    }

    /**
     * Get the alert level color using the follow criteria:
     *
     * Red (level 4) if the incidence was above the high threshold for at
     *  least 5 weeks;
     * Orange (level 3) if above the high threshold from 1 to 4 weeks;
     * Yellow (level 2) if crossed the epidemic threshold but not the high one;
     * Green (level 1) if it did not cross the epidemic threshold.
     * @param {dict} d - total number of alert occurrence
     * @return {number} alert level
     */
    getAlertLevelForWholeYear(d) {
        if (d[4] >= 5) return 4;
        if (d[4] >= 1 && d[4] < 5) return 3;
        if (d[2] >= 1 || d[3] >= 1) return 2;
        return 1;
    }
}


/**
 * When a week mark is changed, this function should update and trigger
 * some information and chart
 * @param {dict} srag_data - srag data
 */
function changeWeek(srag_data) {
    d3.select('#week').on('change', function(){ 
        week = parseInt($('#week').val() || 0);
        year = parseInt($('#year').val() || 0);

        $('.week-display').text(week);
        
        style_properties = {
            fillColor: 'white',
            weight: 1
        };
        
        if(week>0) {
            $("#data-table").removeClass('hidden');
            df = $.grep(srag_data, function(n,i){
                return n.isoweek==week
            });
        } else {
            $("#data-table").addClass('hidden');
            $("#linechart").addClass('hidden');
            $('.week-display').text('');
            df = srag_data;
        }
        
        //print_filter(df);
        changeColorMap(srag_data);
        
        state_name = $('#selected_state').val();

        plot_incidence_chart(year, state_name, week);
        makeTable(year, week, state_name);

    });
}



/**
 * 
 * 
 */
function makeGraphs(
    error, br_states, srag_data
) {    
    makeMap(br_states, srag_data);
    changeWeek(srag_data);
    
    var state_name = $('#selected_state').val();
    var week = parseInt($('#week').val() || 0);
    var year = parseInt($('#year').val() || 0);

    if (state_name) {
        plot_incidence_chart(year, state_name, week);
    }
    
    makeTable(year, week, state_name);
}

userInterface = UserInterface({
    year: $('#year'),
    week: $('#week'),
    state: $('#selected_state'),
    tableContainer: $('#divTable'),
    weekDisplay: $('.week-display'),
    radTypeState: $('#radTypeState')
});

dashboard = new Dashboard(
    userInterface
);

$(document).ready(dashboard.init);