/* -*- Mode: JavaScript; tab-width: 8; indent-tabs-mode: nil;
 c-basic-offset: 2 -*- */
/* vim: set ts=8 sts=2 et sw=2 tw=80: */
/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * Allows control over all dashboard functionalities.
 * @property {string} group_by - Data aggregation criterion (year|week).
 * @property {string} delimitation - Data aggregation criterion (state|region).
 * @property {number} lastWeek - The last week defined (e.g. 2).
 * @property {object} sragData - SRAG data object.
 * @property {SRAGTable} sragTable - SRAGTable object.
 * @property {SRAGMap} sragMap - SRAGMap object.
 * @property {SRAGIncidenceChart} sragIncidenceChart - SRAGIncidenceChart
 *   object.
 * @property {SRAGAgeChart} sragAgeChart - SRAGAgeChart object.
 */


function getTerritoryType() {
    switch ($('input[name="radType[]"]:checked').attr('id')) {
        case 'radTypeState':
            return 'state';
        case 'radTypeRegionGeo':
            return 'region_geo';
        case 'radTypeRegion':
            return 'region';
    }
}

/*
# TODO: properly incorporate regiongeo as in flu_table.js, views.py, index.html
 */
class Dashboard {
  /**
   * @param {dict} lastWeekYears - Dictionary with the last week of each
      available year (e.g. {2015: 53, 2016: 52}).
   */
  constructor(lastWeekYears) {
    var _this = this;
    this.group_by = 'week'; // year or week
    // state or region
    this.delimitation = getTerritoryType();
    this.lastWeek = $('#week').val() || 0;
    this.lastWeekYears = lastWeekYears;
    this.sragData = {};

    // table
    this.sragTable = new SRAGTable();
    this.sragMap = new SRAGMap();
    this.sragIncidenceChart = new SRAGIncidenceChart(
      '#weekly-incidence-curve-chart', this.lastWeekYears
    );

    this.sragAgeChart = new SRAGAgeChart('#age-chart');

    $('#year').change(function () {_this.load_graphs();});

    $('#btn-detailed').click(function(){
      $('#week').attr('min', 1);
      $('#week').val(_this.lastWeek);
      $('#div-week').removeClass('hidden');
      $('#btn-resumed').removeClass('selected');
      $('#btn-detailed').addClass('selected');
      $('.period-display').text('na semana epidemiológica');

      _this.changeWeek();
    });

    $('#btn-resumed').click(function(){
      $('#div-week').addClass('hidden');
      var _week = parseInt($('#week').val() || 0);

      if (_week > 0) {
        _this.lastWeek = _week;
      }

      $('#week').attr('min', 0);
      $('#week').val(0);
      $('#btn-detailed').removeClass('selected');
      $('#btn-resumed').addClass('selected');
      $('.period-display').text('no ano epidemiológico');

      _this.changeWeek();
    });

    // week
    d3.select('#week').on('change', function(){_this.changeWeek();});
    $('#week').on('input', function(){
      $('#week-display').val($('#week').val());
    });
    $('#week-display').change(function(){
      var _week = $('#week-display').val();

      if (!(_week >= 1 && _week <= 52)) {
        $('#week-display').val($('#week').val());
        return;
      }

      $('#week').val($('#week-display').val());
      _this.changeWeek();
    });

    // selection type
    $('#radTypeState').change(function(){
      $('#selected-territory').val('');
      _this.load_graphs();
    });
    $('#radTypeRegion').change(function(){
      $('#selected-territory').val('');
      _this.load_graphs();
    });

    // dataset
    $('#dataset').change(function(){
      _this.load_graphs();
    });

    // scale
    $('#scale').change(function(){
      _this.load_graphs();
    });
  }

  /**
   * starts up the charts
   */
  init() {
    if ($('#btn-detailed').hasClass('selected')) {
      $('#week').attr('min', 1);
      $('#week').val(_this.lastWeek);
      $('#div-week').removeClass('hidden');
      $('#btn-resumed').removeClass('selected');
      $('#btn-detailed').addClass('selected');
      $('.period-display').text('na semana epidemiológica');
    } else {
      $('#div-week').addClass('hidden');
      var _week = parseInt($('#week').val() || 0);

      if (_week > 0) {
        this.lastWeek = _week;
      }

      $('#week').attr('min', 0);
      $('#week').val(0);
      $('#btn-detailed').removeClass('selected');
      $('#btn-resumed').addClass('selected');
      $('.period-display').text('no ano epidemiológico');

    }
    this.load_graphs();
    $('.week-display').text($('#week').val() || 0);
  }

  /**
   * load data and build charts
   */
  load_graphs() {
    var _this = this;

    var fn = function(error, statesBR, sragData){
      _this.sragData = sragData;
      _this.statesBR = statesBR;
      _this.makeGraphs(error);
    };

    var delimitation = getTerritoryType();

    var url = [
        '.', 'data',
        $('#dataset option:selected').val(),
        $('#scale option:selected').val(),
        $('#year').val() || 0,
        delimitation
    ].join('/');

    queue()
      .defer(d3.json, 'static/data/br-states.json')
      .defer(d3.json, url)
      .await(fn);
  }

  /**
   * When a week mark is changed, this function should update the charts and
   * SRAG data table.
   */
  changeWeek() {
    var _this = this;

    var dataset = $('#dataset option:selected').val();
    var scale = $('#scale option:selected').val();
    var week = parseInt($('#week').val() || 0);
    var year = parseInt($('#year').val() || 0);

    $('.week-display').text(week);

    var styleProperties = {
      fillColor: 'white',
      weight: 1
    };

    if(week>0) {
      var df = $.grep(_this.sragData, function(n,i){
          return n.epiweek==week
      });
    } else {
      $('.week-display').text('');
      var df = _this.sragData;
    }

    var territoryName = $('#selected-territory').val() || 'Brasil';

    _this.sragMap.changeColorMap(_this.sragData);
    _this.sragIncidenceChart.plot(dataset, scale, year, week, territoryName);
    _this.sragAgeChart.plot(dataset, scale, year, week, territoryName);
    _this.sragTable.makeTable(dataset, scale, year, week, territoryName);
  }

  /**
   * Trigger the functions to create the charts and the data table.
   * @param {object} error - data about any error.
   */
  makeGraphs(error) {
    var territoryName = $('#selected-territory').val() || 'Brasil';
    var dataset = $('#dataset option:selected').val();
    var scale = $('#scale option:selected').val();
    var week = parseInt($('#week').val() || 0);
    var year = parseInt($('#year').val() || 0);
    var _this = this;

    this.sragMap.makeMap(
      this.statesBR, this.sragData, dataset, scale, year, week,
      function(
        dataset, scale, year, territoryName, week
      ) {
        _this.sragIncidenceChart.plot(dataset, scale, year, week, territoryName);
        _this.sragAgeChart.plot(dataset, scale, year, week, territoryName);
        _this.sragTable.makeTable(dataset, scale, year, week, territoryName);
      }
    );

    this.changeWeek();

    this.sragIncidenceChart.plot(dataset, scale, year, week, territoryName);
    this.sragAgeChart.plot(dataset, scale, year, week, territoryName);
    this.sragTable.makeTable(dataset, scale, year, week, territoryName);
  }
}