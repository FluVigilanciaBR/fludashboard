/* -*- Mode: JavaScript; tab-width: 8; indent-tabs-mode: nil;
 c-basic-offset: 2 -*- */
/* vim: set ts=8 sts=2 et sw=2 tw=80: */
/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// CONSTANTS
DATASET_TITLE = {
    'srag': 'SRAG',
    'sragflu': 'SRAG por Influenza',
    'obitoflu': 'Óbitos por Influenza'
};

/**
 * SRAG Map allows create a map divided by federal states or regions and
 * colored by alert criteria.
 * @property {Object.<string, number>} fluColors - Correspondent color for each
 *   alert level.
 * @property {object} map - Leaflet map object.
 * @property {object} osm - Open Street Map Tile object.
 * @property {object} geojsonLayer - GeoJson object.
 * @property {Object.<string, string>} regionIds.
 * @property {Object.<string, string>} regionNames.
 * @property {object} legend - Leaflet Legend Object.
 */
class SRAGMap {
  /**
   */
  constructor() {
    this.fluColors = {
      1: 'green',
      2: 'yellow',
      3: '#ff7700',
      4: 'red',
    };
    // create the tile layer with correct attribution
    this.map = L.map('map');

    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='Map data © <a href="http://openstreetmap.org">' +
      'OpenStreetMap</a> contributors';

    this.osm = new L.TileLayer(
      osmUrl, {minZoom: 1, maxZoom: 12, attribution: osmAttrib}
    );

    this.map.setView([-16, -50.528742], 3)  ;
    this.osm.addTo(this.map);
    this.geojsonLayer = {};

    this.regionIds = {
      // 1
      'Acre': 'RegN',
      'Amapá': 'RegN',
      'Amazonas': 'RegN',
      'Pará': 'RegN',
      'Rondônia': 'RegN',
      'Roraima': 'RegN',
      // 2
      'Alagoas': 'RegL',
      'Bahia': 'RegL',
      'Ceará': 'RegL',
      'Espírito Santo': 'RegL',
      'Paraíba': 'RegL',
      'Pernambuco': 'RegL',
      'Rio de Janeiro': 'RegL',
      'Rio Grande do Norte': 'RegL',
      'Sergipe': 'RegL',
      // 3
      'Distrito Federal': 'RegC',
      'Goiás': 'RegC',
      'Maranhão': 'RegC',
      'Mato Grosso': 'RegC',
      'Mato Grosso do Sul': 'RegC',
      'Piauí': 'RegC',
      'Tocantins': 'RegC',
      // 4
      'Minas Gerais': 'RegS',
      'Paraná': 'RegS',
      'Rio Grande do Sul': 'RegS',
      'Santa Catarina': 'RegS',
      'São Paulo': 'RegS',
    };

    this.regionNames = {
      'RegC': 'Regional Centro',
      'RegN': 'Regional Norte',
      'RegS': 'Regional Sul',
      'RegL': 'Regional Leste',
    };

    this.legend = new L.Control.Legend({
      position: 'bottomright',
      collapsed: false,
      controlButton: {
        title: "Legend"}
    });

    this.map.addControl(this.legend);
      
    $(".legend-container").append( $("#legend") );
  }

  /**
   * Builds a Brazilian map
   * @param {dict} geoJsonBr - geoJson data about Brazilian territory
   * @param {dict} sragData - SRAG data
   * @param {string} dataset - dataset
   * @param {string} scale - data scale
   */
  makeMap(
    geoJsonBr, sragData, dataset, scale, year, week, clickExternalTrigger
  ) {
    var _this = this;
    var title = '';

    title = (scale == 'incidence') ?
        'Mapa de incidência de ':
        'Mapa de situação de ';
    title = title + DATASET_TITLE[dataset];
    $('#map-incidence-case-title').text(title);

    // remove existent layer from the map
    this.map.eachLayer(function (layer) {
      if ('feature' in layer) {
        _this.map.removeLayer(layer);
      }
    });

    $('.territory-display').text(' - Brasil');

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
          var territoryType = (
            $('input[name="radType[]"]:checked').attr('id') == 'radTypeState' ?
            'state' : 'region'
          );

          if (territoryType=='state') {
            // state
            if ($('#selected-state').val() == stateName) {
              stateName = '';
              $('.territory-display').text(' - Brasil');
            } else {
              // bold the selected state
              layer.setStyle({
                weight: 2
              });
              $('.territory-display').text(' - ' + stateName);
            }
          } else {
            // regions
            var rid = _this.regionIds[stateName];
            var ridName = _this.regionNames[rid];

            _this.geojsonLayer.eachLayer(function (_layer) {
              var _rid = _this.regionIds[_layer.feature.properties.nome];

              _layer.setStyle({color: '#333333'});

              if (_rid == rid && $('#selected-state').val() != ridName) {
                _layer.setStyle({weight: 2});
                _layer.bringToFront();
              } else {
                _layer.setStyle({weight: 1});
              }
            });

            // state
            if ($('#selected-state').val() == ridName) {
              stateName = '';
              $('.territory-display').text(' - Brasil');
            } else {
              $('.territory-display').text(' - ' + ridName);
              stateName = ridName;
            }
          }

          $('#selected-state').val(stateName);

          clickExternalTrigger(dataset, scale, year, stateName, week);
        }
      });
    };

    var selectedState = $('#selected-state').val();
    var territoryType = (
      $('input[name="radType[]"]:checked').attr('id') == 'radTypeState' ?
      'state' : 'region'
    );

    if (territoryType=='state') {
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

          if (weekState != undefined) {
            styleProperties['fillColor'] = _this.fluColors[weekState['alert']];
          }

          if (selectedState==layerName) {
            styleProperties['weight'] = 2;
          }
          return styleProperties;
        }
      });
    } else {
      // region
      this.geojsonLayer = L.geoJson(geoJsonBr, {
        onEachFeature: onEachFeature,
        style: function(feature) {
            var layerName = feature.properties.nome;
            var _rid = _this.regionIds[layerName];

            var styleProperties= {
                fillColor: '#fffff',
                color: '#333333',
                fillOpacity: 0.5,
                weight: 1,
            };

            /*var weekState = $.grep(sragData, function(n,i){
              return (
                n.unidade_da_federacao===layerName &&
                (n.epiweek===week || week==0)
              );
            })[0];

            if (weekState != undefined) {
              styleProperties['fillColor'] = _this.fluColors[weekState['alert']];
            }*/

            if (selectedState==_rid) {
              styleProperties['weight'] = 2;
            }
            return styleProperties;
          }
      });
    }
    this.geojsonLayer.addTo(this.map);
  }

  /**
   * Gets the alert level color using the follow criteria:
   *
   * - Red (level 4) if the incidence was above the high threshold for at
   *   least 5 weeks;
   * - Orange (level 3) if above the high threshold from 1 to 4 weeks;
   * - Yellow (level 2) if crossed the epidemic threshold but not the high one;
   * - Green (level 1) if it did not cross the epidemic threshold.
   * @param {dict} d - Total number of alert occurrence
   * @returns {number} - Alert level (1-4)
   */
  getAlertLevelForWholeYear(d) {
    var high_threshold = d[4] + d[3];

    if (high_threshold >= 5) return 4;
    if (high_threshold > 1) return 3;
    if (d[2] >= 1) return 2;
    return 1;
  }

  /**
   * Changes the color of the map using the alerts criteria
   * @param {dict} df - Data frame object
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

    var territoryType = (
      $('input[name="radType[]"]:checked').attr('id') == 'radTypeState' ?
      'state' : 'region'
    );

    if(week>0) {
      // when by week criteria is selected
      var df_alert = $.grep(df, function(n,i){
        return n.epiweek===week
      });

      this.geojsonLayer.eachLayer(function (layer) {
        var layerName = layer.feature.properties.nome;
        var territoryName = '';

        if (territoryType=='state') {
          territoryName = layerName;
        } else {
          territoryName = _this.regionNames[_this.regionIds[layerName]];
        }

        layer.setStyle(styleProperties);
        if (territoryName==state) {
          layer.setStyle({'weight': 2});
        }

        var df_alert_state = $.grep(df_alert, function(n,i){
          return n.unidade_da_federacao===territoryName
        })[0];

        if (df_alert_state != undefined) {
          layer.setStyle({
            fillColor: _this.fluColors[df_alert_state['alert']]
          });
        }
      });
    } else {
      // when whole year criteria is selected
      this.geojsonLayer.eachLayer(function (layer) {
        var layerName = layer.feature.properties.nome;
        var territoryName = '';

        if (territoryType=='state') {
          territoryName = layerName;
        } else {
          territoryName = _this.regionNames[_this.regionIds[layerName]];
        }

        layer.setStyle(styleProperties);
        if (territoryName==state) {
          layer.setStyle({'weight': 2});
        }

        var alerts = {
          1: 0,
          2: 0,
          3: 0,
          4: 0
        };

        var df_alert_state = $.grep(df, function(n,i){
          return n.unidade_da_federacao===territoryName;
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
