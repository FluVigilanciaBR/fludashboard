/* -*- Mode: JavaScript; tab-width: 8; indent-tabs-mode: nil; c-basic-offset: 2 -*- */
/* vim: set ts=8 sts=2 et sw=2 tw=80: */
/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/** */
class SRAGMap {
  constructor() {
    this.fluColors = {
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

    this.map.setView([-16, -50.528742], 3)  ;
    this.osm.addTo(this.map);
  }

  /**
   * Build a map
   *
   * @param {dict} geoJsonBr - geoJson data about Brazilian territory
   * @param {dict} sragData - srag data
   */
  makeMap(
    geoJsonBr, sragData, year, week, clickExternalTrigger
  ) {
    var fluColors = this.fluColors;
    var map = this.map;
    // remove existent layer from the map
    this.map.eachLayer(function (layer) {
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
          geojsonLayer.eachLayer(function (_layer) {
            _layer.setStyle({
              weight: 1
            });
          });

          var stateName = feature.properties.nome;
          var week = parseInt($('#week').val() || 0);
          var year = parseInt($('#year').val() || 0);

          if ($('#selected-state').val() == stateName) {
            stateName = '';
            $('.incidence-chart-title').text('');
          } else {
            // bold the selected state
            layer.setStyle({
              weight: 2
            });
            $('.incidence-chart-title').text(' - ' + stateName);
          }

          $('#selected-state').val(stateName);

          clickExternalTrigger(year, stateName, week);
        }
      });
    };

    var selectedState = $('#selected-state').val();

    // show geojson on the map
    var geojsonLayer = L.geoJson(geoJsonBr, {
      onEachFeature: onEachFeature,
      style: function(feature) {
        var layerName = feature.properties.nome;

        var styleProperties= {
          fillColor: '#ffffff',
          color: '#333333',
          fillOpacity: 0.5,
          weight: 1,
        };

        var weekState = $.grep(sragData, function(n,i){
          return (
            n.unidade_da_federacao===layerName &&
            n.isoweek===week
          );
        })[0];

        styleProperties['fillColor'] = fluColors[weekState['alert']];

        if (selectedState==layerName) {
          styleProperties['weight'] = 2;
        }
        return styleProperties;
      }
    });
    geojsonLayer.addTo(map);
  }


  /**
   * Change the color of the map using the alerts criteria
   *
   * @param {dict} df - data frame object
   */
  changeColorMap(df) {
    var state = $('#selected-state').val();
    var week = parseInt($('#week').val() || 0);
    var styleProperties= {
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
      geojsonLayer.eachLayer(function (layer) {
        layerName = layer.feature.properties.nome;

        layer.setStyle(styleProperties);
        if (layerName==state) {
          layer.setStyle({'weight': 2});
        }

        df_alert_state = $.grep(df_alert, function(n,i){
          return n.unidade_da_federacao===layerName
        })[0];

        layer.setStyle({
          fillColor: fluColors[df_alert_state['alert']]
        });
      });
    } else {
      // when whole year criteria is selected
      geojsonLayer.eachLayer(function (layer) {
        layerName = layer.feature.properties.nome;

        layer.setStyle(styleProperties);
        if (layerName==state) {
          layer.setStyle({'weight': 2});
        }

        alerts = {
          1: 0,
          2: 0,
          3: 0,
          4: 0
        };

        df_alert_state = $.grep(df, function(n,i){
          return n.unidade_da_federacao===layerName
        });


        $(df_alert_state).each(function(i){
          ++alerts[df_alert_state[i]['alert']];
        });

        layer.setStyle({
          fillColor: fluColors[getAlertLevelForWholeYear(alerts)]
        });
      });
    }
  }
}