var divTableContent = '' +
'<table id="data-table" class="display table table-striped table-condensed">' +
'             <!-- create a custom header -->' +
'                <thead class="header">' +
'                    <tr class="header">' +
'                    <th>Unidade da Federa&ccedil;&atilde;o</th>' +
'                    <th>Semana</th>' +
'                    <th>Incidência (por 100 mil habitantes)</th>' +
'                    </tr>' +
'                </thead>' +
'            </table>';

var flu_colors = {
    1: 'green',
    2: 'yellow',
    3: 'orange',
    4: 'red',
};

var map = L.map('map');

// create the tile layer with correct attribution
var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
var osm = new L.TileLayer(
    osmUrl, {minZoom: 1, maxZoom: 12, attribution: osmAttrib}
);

$('#divTable').html(divTableContent);
var data_table = $('#data-table').DataTable();

/**
 * 
 * 
 */
function init() {
    map.setView([-16, -50.528742], 3);
    osm.addTo(map);
    
    load_graphs();
    
    $('.week-display').text($('#week').val());
}

/**
 * 
 * 
 */
function load_graphs() {
    var year = $('#year').val() || 0;
    var week = $('#week').val() || 0;
    var state = $('#selected_state').val() || '';
    
    queue()
        .defer(d3.json, 'static/data/br-states.json')
        .defer(d3.json, '/data/incidence/' + year)
        .await(makeGraphs);
}

/**
 * 
 * 
 */
function plot_incidence_chart(year, state_name, week) {
    if (state_name == '') {
        $('.chart-incidence').addClass('hidden');
        $('#vi .weekly-incidence-curve-chart').empty();
        return;
    } else {
        $('.chart-incidence').removeClass('hidden');
    }
    
    var chart = c3.generate({
        bindto: '#weekly-incidence-curve-chart',
        data: {
          url: './data/weekly-incidence-curve/' + year + '/' + state_name,
          x: 'isoweek',
          names: {
              corredor_baixo: null,
              corredor_mediano: null,
              corredor_alto: null,
              srag: 'SRAG',
              limiar_pre_epidemico: 'Limiar Pré epidêmico',
              intensidade_alta: 'Intensidade Alta',
              intensidade_muito_alta: 'Intensidade Muito Alta'
          },
          types: {
              corredor_baixo: 'area',
              corredor_mediano: 'area',
              corredor_alto: 'area',
              srag: 'line',
              limiar_pre_epidemico: 'line',
              intensidade_alta: 'line',
              intensidade_muito_alta: 'line'
          },
          colors: {
            corredor_baixo: '#00ff00',
            corredor_mediano: '#ffff00',
            corredor_alto: '#ff9900',
            srag: '#000000',
            limiar_pre_epidemico: '#0000ff',
            intensidade_alta: '#00ff00',
            intensidade_muito_alta: '#ff0000'
          }
        },
        axis: {
          x: {
            label: {
              text: 'SE',
              position: 'outer-center'
            }
          },
          y: {
            label: {
              text: 'Incidência (por 100 mil habitantes)',
              position: 'outer-middle'
            }
          },
        },
        regions: [
            {start:0, end:52, class: 'alert-red'}
        ],
        grid: {                 
          x: {
           lines: [
              {value: week, text: 'Semana Selecionada', position: 'middle'}
            ], show: false
          },
          y: {show: false}
        },/*
        zoom: {
          enabled: true
        },*/ /*
        subchart: {
          show: true
        },*/
        tooltip: {
          show: false
        },
        point: {
          show: false
        }
    });

}

/**
 * Red if the incidence was above the high threshold for at least 5 weeks;
 * Orange if above the high threshold from 1 to 4 weeks;
 * Yellow if crossed the epidemic threshold but not the high one;
 * Green if it did not cross the epidemic threshold.
 */
function alert_level_for_whole_year(d) {
    if (d[4] >= 5) return 4;
    if (d[4] >= 1 && d[4] < 5) return 3;
    if (d[2] >= 1 || d[3] >= 1) return 2;
    return 1;
}

/**
 * 
 * 
 */
function makeMap(br_states, srag_data) {
    week = parseInt($('#week').val() || 0);
    
    map.eachLayer(function (layer) {
        if ('feature' in layer) {
            map.removeLayer(layer);
        }
    });
    
    function onEachFeature(feature, layer) {
        //bind click
        layer.on({
            click: function(){
                // reset line weight
                geojson_layer.eachLayer(function (_layer) {  
                    _layer.setStyle({
                        weight: 1
                    });
                });
                
                var state_name = feature.properties.nome;
                var week = parseInt($('#week').val() || 0);
                var year = parseInt($('#year').val() || 0);
                
                if ($('#selected_state').val() == state_name) {
                    state_name = '';
                    $('.incidence-chart-title').text('');
                } else {
                    // bold the selected state
                    layer.setStyle({
                        weight: 2
                    });
                    $('.incidence-chart-title').text(' - ' + state_name);
                }
                
                $('#selected_state').val(state_name);

                plot_incidence_chart(year, state_name, week);
                makeTable(year, week, state_name);
            }
        });
    };
    
    var selected_state = $('#selected_state').val();
    
    // start the map in South-East England
    geojson_layer = L.geoJson(br_states, {
        onEachFeature: onEachFeature,
        style: function(feature) {
            l_name = feature.properties.nome;
            
            style_properties= {
                fillColor: '#ffffff',
                color: '#333333',
                fillOpacity: 0.5,
                weight: 1,
            };
            
            week_state = $.grep(srag_data, function(n,i){
                return (
                    n.unidade_da_federacao===l_name &&
                    n.isoweek===week
                );
            })[0];
            
            style_properties['fillColor'] = flu_colors[week_state['alert']];
            
            if (selected_state==l_name) {
                style_properties['weight'] = 2;
            }
            return style_properties;
        }
    });
    geojson_layer.addTo(map);
    //osm.addTo(map);
}


/**
 * 
 * 
 */
function changeColorMap(df) {
    var state = $('#selected_state').val();
    var week = parseInt($('#week').val() || 0);
    var style_properties= {
        fillColor: '#ffffff',
        color: '#333333',
        fillOpacity: 0.5,
        weight: 1,
    };
    
    
    if(week>0) {
        df_alert = $.grep(df, function(n,i){
            return n.isoweek===week
        });
        
        geojson_layer.eachLayer(function (layer) {  
            l_name = layer.feature.properties.nome;
            
            layer.setStyle(style_properties);
            if (l_name==state) {
                layer.setStyle({'weight': 2});
            }
        
            df_alert_state = $.grep(df_alert, function(n,i){
                return n.unidade_da_federacao===l_name
            })[0];
            
            layer.setStyle({
                fillColor: flu_colors[df_alert_state['alert']]
            });
        });
    } else {
        geojson_layer.eachLayer(function (layer) {  
            l_name = layer.feature.properties.nome;
            
            layer.setStyle(style_properties);
            if (l_name==state) {
                layer.setStyle({'weight': 2});
            }
            
            alerts = {
                1: 0,
                2: 0,
                3: 0,
                4: 0
            };
            
            df_alert_state = $.grep(df, function(n,i){
                return n.unidade_da_federacao===l_name
            });
            
            
            $(df_alert_state).each(function(i){ 
                ++alerts[df_alert_state[i]['alert']];
            });
            
            layer.setStyle({
                fillColor: flu_colors[alert_level_for_whole_year(alerts)]
            });
        
        });
    }
}

/**
 * 
 * 
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
function makeTable(year, week, state_name) {
    var columns = [];
    var _tmp = '';
    var table_settings = {
        "dom": 'Bfrtip',
        "language": {
            "url": "/static/libs/datatables/i18n/Portuguese-Brasil.json"
        },
        "buttons": [
            'excelHtml5',
            'csvHtml5'
        ],
        "pageLength": 10
    };
    
    table_settings['columnDefs'] = [];
    
    if (state_name) {
        _tmp = '/' + state_name;
        table_settings['columnDefs'].push({
            "targets": [ 0 ],
            "visible": false,
            "searchable": false
        });
    }
    
    if (week > 0) {
        table_settings['columnDefs'].push({
            "targets": [ 1 ],
            "visible": false,
            "searchable": false
        });
    }
    
    table_settings['ajax'] = '/data/data-table/' + year + '/' + week + _tmp;
    table_settings['columns'] = [
        {'data': 'unidade_da_federacao'},
        {'data': 'isoweek'}, 
        {'data': 'srag'}
    ];
    
    // destroy old table
    data_table.destroy();
    $('#data-table').empty(); // empty in case the columns change
    
    delete data_tables;
    
    // create new table
    $('#divTable').html(divTableContent);
    data_table = $('#data-table').DataTable(table_settings);
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

$(document).ready(init);
$('#year').change(load_graphs);