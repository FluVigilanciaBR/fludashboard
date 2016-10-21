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
    this.geojsonLayer = {};
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
    var _this = this;

    // remove existent layer from the map
    this.map.eachLayer(function (layer) {
      if ('feature' in layer) {
        _this.map.removeLayer(layer);
      }
    });

    // apply onclick event on each region/state on the map
    function onEachFeature(feature, layer) {
      //bind click
      layer.on({
        click: function(){
          // reset line weight
          _this.geojsonLayer.eachLayer(function (_layer) {
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
    this.geojsonLayer = L.geoJson(geoJsonBr, {
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
            (n.epiweek===week || week==0)
          );
        })[0];

        styleProperties['fillColor'] = _this.fluColors[weekState['alert']];

        if (selectedState==layerName) {
          styleProperties['weight'] = 2;
        }
        return styleProperties;
      }
    });
    this.geojsonLayer.addTo(this.map);
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

  /**
   * Change the color of the map using the alerts criteria
   *
   * @param {dict} df - data frame object
   */
  changeColorMap(df) {
    var _this = this;
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
      var df_alert = $.grep(df, function(n,i){
        return n.epiweek===week
      });

      this.geojsonLayer.eachLayer(function (layer) {
        var layerName = layer.feature.properties.nome;

        layer.setStyle(styleProperties);
        if (layerName==state) {
          layer.setStyle({'weight': 2});
        }

        var df_alert_state = $.grep(df_alert, function(n,i){
          return n.unidade_da_federacao===layerName
        })[0];

        layer.setStyle({
          fillColor: _this.fluColors[df_alert_state['alert']]
        });
      });
    } else {
      // when whole year criteria is selected
      this.geojsonLayer.eachLayer(function (layer) {
        var layerName = layer.feature.properties.nome;

        layer.setStyle(styleProperties);
        if (layerName==state) {
          layer.setStyle({'weight': 2});
        }

        var alerts = {
          1: 0,
          2: 0,
          3: 0,
          4: 0
        };

        var df_alert_state = $.grep(df, function(n,i){
          return n.unidade_da_federacao===layerName
        });


        $(df_alert_state).each(function(i){
          ++alerts[df_alert_state[i]['alert']];
        });

        layer.setStyle({
          fillColor: _this.fluColors[_this.getAlertLevelForWholeYear(alerts)]
        });
      });
    }
  }
}