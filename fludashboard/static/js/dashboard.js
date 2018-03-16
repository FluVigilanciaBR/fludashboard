/* -*- Mode: JavaScript; tab-width: 8; indent-tabs-mode: nil;
 c-basic-offset: 2 -*- */
/* vim: set ts=8 sts=2 et sw=2 tw=80: */
/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * Allows control over all dashboard functionalities.
 * @property {string} group_by - Data aggregation criterion (year|week).
 * @property {string} territoryTypeId - Data aggregation criterion (state|region).
 * @property {number} lastWeek - The last week defined (e.g. 2).
 * @property {object} sragData - SRAG data object.
 * @property {SRAGTable} sragTable - SRAGTable object.
 * @property {SRAGMap} sragMap - SRAGMap object.
 * @property {SRAGIncidenceChart} sragIncidenceChart - SRAGIncidenceChart
 *   object.
 * @property {SRAGAgeChart} sragAgeChart - SRAGAgeChart object.
 */


function getTerritoryTypeId() {
    return parseInt(
        $('input[name="radTerritoryType[]"]:checked').val()
    );
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
    this.territoryTypeId = getTerritoryTypeId();
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
      _this.prepare_detailed_dashboard();
      _this.changeWeek();
    });

    $('#btn-resumed').click(function(){
      _this.prepare_resumed_dashboard();
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
    $('#radTerritoryTypeState').change(function(){
      $('#selected-territory').val('');
      _this.load_graphs();
    });
    $('#radTerritoryTypeRegion').change(function(){
      $('#selected-territory').val('');
      _this.load_graphs();
    });
    $('#radTerritoryTypeRegional').change(function(){
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
      this.prepare_detailed_dashboard();
    } else if ($('#btn-resumed').hasClass('selected')) {
      this.prepare_resumed_dashboard();
    } else {
      this.prepare_contingency_dashboard();
    }

    this.load_graphs();
    $('.week-display').text($('#week').val() || 0);
  }


  prepare_detailed_dashboard() {
      $('#week').attr('min', 1);
      $('#week').val(this.lastWeek);
      $('#div-week').removeClass('hidden');
      $('#div-year').removeClass('hidden');
      $('#div-dataset').removeClass('hidden');
      $('#div-scale').removeClass('hidden');

      $('#btn-resumed').removeClass('selected');
      $('#btn-contingency').removeClass('selected');
      $('#btn-detailed').addClass('selected');

      $('.period-display').text('na semana epidemiológica');
  }

  prepare_resumed_dashboard() {
      $('#div-week').addClass('hidden');
      $('#div-year').removeClass('hidden');
      $('#div-dataset').removeClass('hidden');
      $('#div-scale').removeClass('hidden');

      var _week = parseInt($('#week').val() || 0);

      if (_week > 0) {
        this.lastWeek = _week;
      }

      $('#week').attr('min', 0);
      $('#week').val(0);

      $('#btn-detailed').removeClass('selected');
      $('#btn-contingency').removeClass('selected');
      $('#btn-resumed').addClass('selected');

      $('.period-display').text('no ano epidemiológico');
  }

  prepare_contingency_dashboard() {
      $('#div-week').addClass('hidden');
      $('#div-year').addClass('hidden');
      $('#div-dataset').addClass('hidden');
      $('#div-scale').addClass('hidden');

      var _week = parseInt($('#week').val() || 0);

      if (_week > 0) {
        this.lastWeek = _week;
      }

      $('#week').attr('min', 0);
      $('#week').val(0);

      $('#btn-detailed').removeClass('selected');
      $('#btn-resumed').removeClass('selected');
      $('#btn-contingency').addClass('selected');

      $('.period-display').text('no ano epidemiológico');
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

    var territoryTypeId = getTerritoryTypeId();

    var url = [
        '.', 'data',
        $('input.view_name.selected').attr('id').substring(4,),
        $('#dataset option:selected').val(),
        $('#scale option:selected').val(),
        $('#year').val() || 0,
        territoryTypeId
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
    var territoryName = $('#selected-territory').val() || 'Brasil';
    var view_name = $('input.view_name.selected').attr('id').substring(4,);

    $('.week-display').text(week);

    var styleProperties = {
      fillColor: 'white',
      weight: 1
    };

    var etiological_url = encodeURI([
        '.', 'data',
        view_name,
        dataset,
        scale,
        year,
        week,
        territoryName,
        'etiological-agents'
    ].join('/'));

    // opportunities chart
    var opportunities_url = encodeURI([
        '.', 'data',
        view_name,
        dataset,
        scale,
        year,
        week,
        territoryName,
        'opportunities-boxplot'
    ].join('/'));


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
    _this.sragIncidenceChart.plot(
        view_name, dataset, scale, year, week, territoryName
    );
    _this.sragAgeChart.plot(
        view_name, dataset, scale, year, week, territoryName
    );
    _this.sragTable.makeTable(
        view_name, dataset, scale, year, week, territoryName
    );

    $('#etiological-chart').load(etiological_url);
    $('#opportunities-chart').load(opportunities_url);
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
    var view_name = $('input.view_name.selected').attr('id').substring(4,);
    var _this = this;

    this.sragMap.makeMap(
      this.statesBR, this.sragData, view_name, dataset, scale, year, week,
      function(
        view_name, dataset, scale, year, territoryName, week
      ) {
        _this.sragIncidenceChart.plot(
            view_name, dataset, scale, year, week, territoryName
        );
        _this.sragAgeChart.plot(
            view_name, dataset, scale, year, week, territoryName
        );
        _this.sragTable.makeTable(
            view_name, dataset, scale, year, week, territoryName
        );

        // etiological chart
        var etiological_url = encodeURI([
            '.', 'data',
            view_name,
            dataset,
            scale,
            year,
            week,
            territoryName,
            'etiological-agents'
        ].join('/'));
        $('#etiological-chart').load(etiological_url);

        // opportunities chart
        var opportunities_url = encodeURI([
            '.', 'data',
            view_name,
            dataset,
            scale,
            year,
            week,
            territoryName,
            'opportunities-boxplot'
        ].join('/'));
        $('#opportunities-chart').load(opportunities_url);

      }
    );

    this.changeWeek();
  }
}