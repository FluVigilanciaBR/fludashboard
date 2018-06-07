/* -*- Mode: JavaScript; tab-width: 8; indent-tabs-mode: nil;
 c-basic-offset: 2 -*- */
/* vim: set ts=8 sts=2 et sw=2 tw=80: */
/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// CONSTANTS
DATASET_TITLE = {
    1: 'SRAG',
    2: 'SRAG por Influenza',
    3: 'Óbitos por Influenza'
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
        'resumed': {
            1: '#ffffcc',
            2: '#c2e699',
            3: '#78c679',
            4: '#238443'
        }, 'detailed': {
            1: '#edf8fb',
            2: '#b3cde3',
            3: '#9f8cc6',
            4: '#88419d'
        }, 'contingency':{
            1: '#ffffcc',
            2: '#a1dab4',
            3: '#41b6c4',
            4: '#225ea8'
        }
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

    this.regionalIds = {
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

    this.regionalNames = {
      'RegC': 'Regional Centro',
      'RegN': 'Regional Norte',
      'RegS': 'Regional Sul',
      'RegL': 'Regional Leste',
    };

    this.regionIds = {
      // 1
      'Acre': 'N',
      'Amapá': 'N',
      'Amazonas': 'N',
      'Pará': 'N',
      'Rondônia': 'N',
      'Roraima': 'N',
      'Tocantins': 'N',
      // 2
      'Alagoas': 'NE',
      'Bahia': 'NE',
      'Ceará': 'NE',
      'Maranhão': 'NE',
      'Paraíba': 'NE',
      'Pernambuco': 'NE',
      'Piauí': 'NE',
      'Rio Grande do Norte': 'NE',
      'Sergipe': 'NE',
      // 3
      'Espírito Santo': 'SE',
      'Rio de Janeiro': 'SE',
      'São Paulo': 'SE',
      'Minas Gerais': 'SE',
      // 4
      'Paraná': 'S',
      'Rio Grande do Sul': 'S',
      'Santa Catarina': 'S',
      // 5
      'Distrito Federal': 'CO',
      'Goiás': 'CO',
      'Mato Grosso': 'CO',
      'Mato Grosso do Sul': 'CO',
    };

    this.regionNames = {
      'N': 'Norte',
      'NE': 'Nordeste',
      'SE': 'Sudeste',
      'CO': 'Centro-oeste',
      'S': 'Sul',
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
    geoJsonBr, sragData, view_name, dataset, scale,
    year, week, clickExternalTrigger
  ) {
    var _this = this;
    var title = '';
    var level_col = (view_name == 'contingency') ? 'contingency' : 'alert';
    var selectedTerritory = $('#selected-territory').val() || 'Brasil';
    var territoryTypeId = getTerritoryTypeId();

    if (view_name == 'contingency'){
      title = 'Mapa do Plano de Contingência';
    } else if (view_name == 'resumed'){
      title = 'Mapa da Temporada para ';
    } else {
      title = (scale == 1) ?
        'Mapa de incidência de ':
        'Mapa de situação de ';
    }

    if (view_name != 'contingency'){
      if (dataset == 1) {
        title = title + DATASET_TITLE[dataset];
      } else {
        title = (
          title + DATASET_TITLE[dataset] +
          " (diagnóstico laboratorial ou clínico-epidemiológico)"
        );
      }
    }
    $('#map-incidence-case-title').text(title);

    // remove existent layer from the map
    this.map.eachLayer(function (layer) {
      if ('feature' in layer) {
        _this.map.removeLayer(layer);
      }
    });

    $('.territory-display').text(' - ' + selectedTerritory);

    // apply onclick event on each region/state on the map
    function onEachFeature(feature, layer) {
      //bind click
      layer.on({
        click: function(){
          // reset line weight
          _this.geojsonLayer.eachLayer(function (_layer) {
            _layer.setStyle({
              weight: 1,
              fillOpacity: 0.7
            });
          });

          var territoryName = feature.properties.nome;
          var week = parseInt($('#week').val() || 0);
          var year = parseInt($('#year').val() || 0);
          var territoryTypeId = getTerritoryTypeId();

          if (territoryTypeId==1) {
            // state
            if ($('#selected-territory').val() == territoryName) {
              territoryName = '';
              $('.territory-display').text(' - Brasil');
              _this.geojsonLayer.eachLayer(function (_layer) {
                _layer.setStyle({
                  weight: 1,
                  fillOpacity: 1
                });
              });
            } else {
              // bold the selected state
              layer.setStyle({
                weight: 3,
                fillOpacity: 1
              });
              $('.territory-display').text(' - ' + territoryName);
            }
          } else if (territoryTypeId==2) {
            // regions
            var rid = _this.regionalIds[territoryName];
            var ridName = _this.regionalNames[rid];

            _this.geojsonLayer.eachLayer(function (_layer) {
              var _rid = _this.regionalIds[_layer.feature.properties.nome];

              _layer.setStyle({color: '#333333', fillOpacity: 0.7});

              if (_rid == rid && $('#selected-territory').val() != ridName) {
                _layer.setStyle({weight: 3, fillOpacity: 1});
                _layer.bringToFront();
              } else {
                _layer.setStyle({weight: 1, fillOpacity: 0.7});
              }
            });

            // state
            if ($('#selected-territory').val() == ridName) {
              territoryName = '';
              _this.geojsonLayer.eachLayer(function (_layer) {
                _layer.setStyle({
                   weight: 1,
                   fillOpacity: 1
                });
              });
              $('.territory-display').text(' - Brasil');
            } else {
              $('.territory-display').text(' - ' + ridName);
              territoryName = ridName;
            }
          } else {
            // geopolitical regions
            var rid = _this.regionIds[territoryName];
            var ridName = _this.regionNames[rid];

            _this.geojsonLayer.eachLayer(function (_layer) {
              var _rid = _this.regionIds[_layer.feature.properties.nome];

              _layer.setStyle({color: '#333333', fillOpacity: 1});

              if (_rid == rid && $('#selected-territory').val() != ridName) {
                _layer.setStyle({weight: 3, fillOpacity: 1});
                _layer.bringToFront();
              } else {
                _layer.setStyle({weight: 1, fillOpacity: 0.7});
              }
            });

            // state
            if ($('#selected-territory').val() == ridName) {
              territoryName = '';
              _this.geojsonLayer.eachLayer(function (_layer) {
                _layer.setStyle({
                  weight: 1,
                  fillOpacity: 1
                });
              });
              $('.territory-display').text(' - Brasil');
            } else {
              $('.territory-display').text(' - ' + ridName);
              territoryName = ridName;
            }
          }

          if (territoryName == '') {
            territoryName = 'Brasil'
          }

          $('#selected-territory').val(territoryName);

          clickExternalTrigger(view_name, dataset, scale, year, territoryName, week);
        }
      });
    };

    if (territoryTypeId==1) {
      // show geojson on the map
      this.geojsonLayer = L.geoJson(geoJsonBr, {
        onEachFeature: onEachFeature,
        style: function(feature) {
          var layerName = feature.properties.nome;

          var styleProperties= {
            fillColor: '#ffffff',
            color: '#333333',
            fillOpacity: 1,
            weight: 1
          };

          var weekState = $.grep(sragData, function(n,i){
            return (
              n.territory_name===layerName &&
              (n.epiweek===week || week==0)
            );
          })[0];

          if (weekState != undefined) {
            styleProperties['fillOpacity'] = 1;
            styleProperties['fillColor'] = (
                _this.fluColors[view_name][weekState[level_col]]
            );
          }

          if (selectedTerritory==layerName) {
            styleProperties['weight'] = 3;
            styleProperties['fillOpacity'] = 1;
          }
          return styleProperties;
        }
      });
    } else if (territoryTypeId==2) {
      // region
      this.geojsonLayer = L.geoJson(geoJsonBr, {
        onEachFeature: onEachFeature,
        style: function(feature) {
            var layerName = feature.properties.nome;
            var _rid = _this.regionalIds[layerName];

            var styleProperties= {
                fillColor: '#fffff',
                color: '#333333',
                fillOpacity: 1,
                weight: 1
            };

            /*var weekState = $.grep(sragData, function(n,i){
              return (
                n.territory_name===layerName &&
                (n.epiweek===week || week==0)
              );
            })[0];

            if (weekState != undefined) {
              styleProperties['fillColor'] = _this.fluColors[weekState[level_col]];
            }*/

            if (selectedTerritory==_rid) {
              styleProperties['weight'] = 3;
              styleProperties['fillOpacity'] = 1;
            }
            return styleProperties;
          }
      });
    } else {
      // geopolitical region
      this.geojsonLayer = L.geoJson(geoJsonBr, {
        onEachFeature: onEachFeature,
        style: function(feature) {
            var layerName = feature.properties.nome;
            var _rid = _this.regionIds[layerName];

            var styleProperties= {
                fillColor: '#fffff',
                color: '#333333',
                fillOpacity: 1,
                weight: 1
            };

            /*var weekState = $.grep(sragData, function(n,i){
              return (
                n.territory_name===layerName &&
                (n.epiweek===week || week==0)
              );
            })[0];

            if (weekState != undefined) {
              styleProperties['fillColor'] = _this.fluColors[weekState[level_col]];
            }*/

            if (selectedTerritory==_rid) {
              styleProperties['weight'] = 3;
              styleProperties['fillOpacity'] = 1;
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
    if (high_threshold >= 1) return 3;
    if (d[2] >= 1) return 2;
    return 1;
  }

  /**
   * Changes the color of the map using the alerts criteria
   * @param {dict} df - Data frame object
   */
  changeColorMap(df) {
    var _this = this;
    var state = $('#selected-territory').val();
    var week = parseInt($('#week').val() || 0);
    var view_name = $('input.view_name.selected').attr('id').substring(4,);
    var level_col = 'alert';
    var styleProperties= {
      fillColor: '#ffffff',
      color: '#333333',
      fillOpacity: 1,
      weight: 1,
    };

    var territoryTypeId = getTerritoryTypeId();

    if(week>0) {
      // when by week criteria is selected
      var df_alert = $.grep(df, function(n,i){
        return n.epiweek===week
      });

      this.geojsonLayer.eachLayer(function (layer) {
        var layerName = layer.feature.properties.nome;
        var territoryName = '';

        if (territoryTypeId==1) {
          territoryName = layerName;
        } else if (territoryTypeId==2) {
          territoryName = _this.regionalNames[_this.regionalIds[layerName]];
        } else {
          territoryName = _this.regionNames[_this.regionIds[layerName]];
        }

        layer.setStyle(styleProperties);
        if (territoryName==state) {
          layer.setStyle({weight: 3});
        }

        var df_alert_state = $.grep(df_alert, function(n,i){
          return n.territory_name===territoryName
        })[0];

        if (df_alert_state != undefined) {
          layer.setStyle({
            fillOpacity: 1,
            fillColor: (
                _this.fluColors[view_name][df_alert_state[level_col]]
            )
          });
        }
      });
    } else {
      // when whole year criteria is selected
      this.geojsonLayer.eachLayer(function (layer) {
        var layerName = layer.feature.properties.nome;
        var territoryName = '';

        if (territoryTypeId==1) {
          territoryName = layerName;
        } else if (territoryTypeId==2) {
          territoryName = _this.regionalNames[_this.regionalIds[layerName]];
        } else {
          territoryName = _this.regionNames[_this.regionIds[layerName]];
        }

        layer.setStyle(styleProperties);
        if (territoryName==state) {
          layer.setStyle({weight: 3});
        }

        var df_alert_state = $.grep(df, function(n,i){
          return n.territory_name===territoryName;
        })[0];

        level_col = (view_name == 'contingency') ? 'contingency' : 'season_level';

        layer.setStyle({
          fillOpacity: 1,
          fillColor: (
            _this.fluColors[view_name][df_alert_state[level_col]]
          )
        });

      });
    }
  }
}
