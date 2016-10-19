/** */
class SRAGMap {

    /**
     * Build a map
     *
     * @param {dict} geoJsonBr - geoJson data about Brazilian territory
     * @param {dict} srag_data - srag data
     */
    static makeMap(
        map, geoJsonBr, srag_data, year, week
    ) {

        // remove existent layer from the map
        map.eachLayer(function (layer) {
            if ('feature' in layer) {
                map.removeLayer(layer);
            }
        });

        // apply onclick event on each region/state on the map
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

        // show geojson on the map
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
    }


    /**
     * Change the color of the map using the alerts criteria
     *
     * @param {dict} df - data frame object
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
            // when by week criteria is selected
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
            // when whole year criteria is selected
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
                    fillColor: flu_colors[getAlertLevelForWholeYear(alerts)]
                });

            });
        }
    }
}